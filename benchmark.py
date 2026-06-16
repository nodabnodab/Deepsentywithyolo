import os
import time
import subprocess
import re
import shutil
import cv2
import matplotlib.pyplot as plt
import numpy as np
from ultralytics import YOLO

# Paths configuration
WORKSPACE = "/workspace"
TEMP_FRAMES_DIR = os.path.join(WORKSPACE, "temp_frames")
OUTPUT_FRAMES_DIR = os.path.join(WORKSPACE, "output_frames")
RESULTS_DIR = os.path.join(WORKSPACE, "inference_results")

# Accuracy Test Videos configuration (with specific frame offsets)
ACC_VIDEOS = {
    "boar": {
        "path": os.path.join(WORKSPACE, "boar_cam.mp4"),
        "ss": "00:00:43",  # Frame ~1300 (where the boar is clearly visible)
        "target_coco_class": None,
        "target_custom_class": 1,
        "display_name": "Wild Boar Video (멧돼지)"
    },
    "waterdeer": {
        "path": os.path.join(WORKSPACE, "waterdeersample.mp4"),
        "ss": "00:00:02",  # Frame ~60 (where the waterdeer is clearly visible)
        "target_coco_class": None,
        "target_custom_class": 2,
        "display_name": "Waterdeer Video (고라니)"
    }
}

MODELS = {
    "best": {
        "pt_path": os.path.join(WORKSPACE, "best.pt"),
        "engine_type": "best",
        "name": "Custom WildLife (best.pt)"
    },
    "yolov8n": {
        "pt_path": os.path.join(WORKSPACE, "yolov8n.pt"),
        "engine_type": "yolov8n",
        "name": "Pure YOLOv8n"
    },
    "yolov11n": {
        "pt_path": os.path.join(WORKSPACE, "yolov11n.pt"),
        "engine_type": "yolov11n",
        "name": "Pure YOLOv11n"
    }
}

def extract_frames(video_path, ss=None, num_frames=300):
    if os.path.exists(TEMP_FRAMES_DIR):
        shutil.rmtree(TEMP_FRAMES_DIR)
    os.makedirs(TEMP_FRAMES_DIR, exist_ok=True)
    
    cmd = ["ffmpeg", "-y"]
    if ss:
        cmd.extend(["-ss", ss])
    cmd.extend([
        "-i", video_path, 
        "-vframes", str(num_frames), 
        os.path.join(TEMP_FRAMES_DIR, "frame_%04d.jpg")
    ])
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return sorted([os.path.join(TEMP_FRAMES_DIR, f) for f in os.listdir(TEMP_FRAMES_DIR) if f.endswith('.jpg')])

def run_python_benchmark(model_key, frame_paths, mode="FP32", is_accuracy_test=False, video_key=None):
    model_info = MODELS[model_key]
    
    # Load model
    model = YOLO(model_info["pt_path"])
    
    # Warmup
    dummy_img = cv2.imread(frame_paths[0])
    model(dummy_img, half=(mode == "FP16"), verbose=False)
    
    # Run
    start_time = time.time()
    correct_detections = 0
    total_frames = len(frame_paths)
    
    for path in frame_paths:
        img = cv2.imread(path)
        if img is None:
            continue
        results = model(img, half=(mode == "FP16"), conf=0.25, iou=0.45, verbose=False)
        
        if is_accuracy_test and video_key:
            video_info = ACC_VIDEOS[video_key]
            detected = False
            if len(results) > 0 and len(results[0].boxes) > 0:
                for box in results[0].boxes:
                    cls_id = int(box.cls[0].item())
                    if model_key == "best":
                        if cls_id == video_info["target_custom_class"]:
                            detected = True
                            break
                    else:
                        # Pure COCO models do not have boar/waterdeer, so correct detection is always False
                        pass
            if detected:
                correct_detections += 1
            
    end_time = time.time()
    total_duration = (end_time - start_time) * 1000.0 # ms
    avg_latency = total_duration / total_frames
    avg_fps = 1000.0 / avg_latency
    detection_rate = (correct_detections / total_frames) * 100.0 if is_accuracy_test else 0.0
    
    return avg_latency, avg_fps, detection_rate

def run_cpp_benchmark(model_key, frame_paths):
    model_info = MODELS[model_key]
    binary_path = os.path.join(WORKSPACE, "cpp/build/deepsenty_inference")
    
    if os.path.exists(OUTPUT_FRAMES_DIR):
        shutil.rmtree(OUTPUT_FRAMES_DIR)
    os.makedirs(OUTPUT_FRAMES_DIR, exist_ok=True)
    
    cmd = [binary_path, model_info["engine_type"], TEMP_FRAMES_DIR, OUTPUT_FRAMES_DIR]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    output = result.stdout
    
    latency_match = re.search(r"Average Latency:\s*([0-9.]+)\s*ms", output)
    fps_match = re.search(r"Average Throughput:\s*([0-9.]+)\s*FPS", output)
    
    if latency_match and fps_match:
        avg_latency = float(latency_match.group(1))
        avg_fps = float(fps_match.group(1))
        return avg_latency, avg_fps
    else:
        print(f"[!] C++ runner execution failed for model {model_key}")
        print("Stdout:", output)
        print("Stderr:", result.stderr)
        return None, None

def generate_charts(speed_data, accuracy_data):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.rcParams.update({'font.size': 12})
    
    categories = ['Python FP32', 'Python FP16', 'TensorRT C++ FP16']
    x = np.arange(len(categories))
    width = 0.25
    
    # Chart 1: Throughput (FPS) Comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width, [speed_data["best"]["FP32"][1], speed_data["best"]["FP16"][1], speed_data["best"]["TRT_CPP"][1]], width, label='Custom Model (best)', color='#2ca02c')
    rects2 = ax.bar(x, [speed_data["yolov8n"]["FP32"][1], speed_data["yolov8n"]["FP16"][1], speed_data["yolov8n"]["TRT_CPP"][1]], width, label='YOLOv8n', color='#1f77b4')
    rects3 = ax.bar(x + width, [speed_data["yolov11n"]["FP32"][1], speed_data["yolov11n"]["FP16"][1], speed_data["yolov11n"]["TRT_CPP"][1]], width, label='YOLOv11n', color='#ff7f0e')
    
    ax.set_ylabel('Throughput (Frames Per Second)')
    ax.set_title('Inference Speed Comparison (Higher is Better)')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    
    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
            
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "throughput_fps.png"), dpi=300)
    plt.close()
    
    # Chart 2: Latency (ms) Comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width, [speed_data["best"]["FP32"][0], speed_data["best"]["FP16"][0], speed_data["best"]["TRT_CPP"][0]], width, label='Custom Model (best)', color='#2ca02c')
    rects2 = ax.bar(x, [speed_data["yolov8n"]["FP32"][0], speed_data["yolov8n"]["FP16"][0], speed_data["yolov8n"]["TRT_CPP"][0]], width, label='YOLOv8n', color='#1f77b4')
    rects3 = ax.bar(x + width, [speed_data["yolov11n"]["FP32"][0], speed_data["yolov11n"]["FP16"][0], speed_data["yolov11n"]["TRT_CPP"][0]], width, label='YOLOv11n', color='#ff7f0e')
    
    ax.set_ylabel('Latency (milliseconds)')
    ax.set_title('Inference Latency Comparison (Lower is Better)')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    
    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}ms',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
            
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "latency_ms.png"), dpi=300)
    plt.close()

    # Chart 3: Target Wildlife Detection Success Rate (%)
    videos_list = ['Wild Boar', 'Waterdeer']
    x_acc = np.arange(len(videos_list))
    
    fig, ax = plt.subplots(figsize=(8, 6))
    rects1 = ax.bar(x_acc - width, [accuracy_data["best"]["boar"], accuracy_data["best"]["waterdeer"]], width, label='Custom Model (best)', color='#2ca02c')
    rects2 = ax.bar(x_acc, [accuracy_data["yolov8n"]["boar"], accuracy_data["yolov8n"]["waterdeer"]], width, label='YOLOv8n (COCO)', color='#1f77b4')
    rects3 = ax.bar(x_acc + width, [accuracy_data["yolov11n"]["boar"], accuracy_data["yolov11n"]["waterdeer"]], width, label='YOLOv11n (COCO)', color='#ff7f0e')
    
    ax.set_ylabel('Correct Class Detection Rate (%)')
    ax.set_title('Wildlife Detection Success Rate Comparison (Higher is Better)')
    ax.set_xticks(x_acc)
    ax.set_xticklabels(videos_list)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)
    
    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
            
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "detection_accuracy.png"), dpi=300)
    plt.close()

def main():
    print("=== Starting Comprehensive Benchmarking (Optimized Offsets) ===")
    
    speed_results = {
        "best": {"FP32": None, "FP16": None, "TRT_CPP": None},
        "yolov8n": {"FP32": None, "FP16": None, "TRT_CPP": None},
        "yolov11n": {"FP32": None, "FP16": None, "TRT_CPP": None}
    }
    
    accuracy_results = {
        "best": {"boar": 0.0, "waterdeer": 0.0},
        "yolov8n": {"boar": 0.0, "waterdeer": 0.0},
        "yolov11n": {"boar": 0.0, "waterdeer": 0.0}
    }
    
    # 1. Evaluate Speeds (using Black Bear Video - first 300 frames)
    print("\n[*] Step 1: Evaluating Speed Metrics (300 frames of Bear Video)...")
    bear_paths = extract_frames(os.path.join(WORKSPACE, "blackbearsample.mp4"), num_frames=300)
    
    for m_key in MODELS.keys():
        print(f"\n--- Model: {MODELS[m_key]['name']} ---")
        
        # Python FP32
        print("Running Python FP32 benchmark...")
        latency, fps, _ = run_python_benchmark(m_key, bear_paths, mode="FP32", is_accuracy_test=False)
        speed_results[m_key]["FP32"] = (latency, fps)
        print(f"-> FP32 Latency: {latency:.2f} ms | FPS: {fps:.1f}")
        
        # Python FP16
        print("Running Python FP16 benchmark...")
        latency, fps, _ = run_python_benchmark(m_key, bear_paths, mode="FP16", is_accuracy_test=False)
        speed_results[m_key]["FP16"] = (latency, fps)
        print(f"-> FP16 Latency: {latency:.2f} ms | FPS: {fps:.1f}")
        
        # C++ TRT FP16
        print("Running C++ TensorRT FP16 benchmark...")
        latency, fps = run_cpp_benchmark(m_key, bear_paths)
        if latency is not None:
            speed_results[m_key]["TRT_CPP"] = (latency, fps)
            print(f"-> C++ TRT Latency: {latency:.2f} ms | FPS: {fps:.1f}")
            
    # 2. Evaluate Accuracy/Detection Rates on boar and waterdeer videos
    print("\n[*] Step 2: Evaluating Wildlife Detection Accuracy...")
    for v_key, v_info in ACC_VIDEOS.items():
        print(f"\n--- Testing Video: {v_info['display_name']} ---")
        paths = extract_frames(v_info["path"], ss=v_info["ss"], num_frames=300)
        
        for m_key in MODELS.keys():
            _, _, det_rate = run_python_benchmark(m_key, paths, mode="FP16", is_accuracy_test=True, video_key=v_key)
            accuracy_results[m_key][v_key] = det_rate
            print(f"Model {MODELS[m_key]['name']}: Correct Detection Rate = {det_rate:.1f}%")
            
    # 3. Generate Visualizations
    print("\n[*] Step 3: Generating comparison charts...")
    generate_charts(speed_results, accuracy_results)
    print(f"Charts saved to {RESULTS_DIR}")
    
    # 4. Clean up
    print("\n[*] Cleaning up temporary directories...")
    if os.path.exists(TEMP_FRAMES_DIR):
        shutil.rmtree(TEMP_FRAMES_DIR)
    if os.path.exists(OUTPUT_FRAMES_DIR):
        shutil.rmtree(OUTPUT_FRAMES_DIR)
    print("[*] Cleanup complete.")
    
    # Print Markdown Summary Tables
    print("\n" + "="*40)
    print("### SPEED COMPARISON TABLE")
    print("| Model | Python FP32 (Latency / FPS) | Python FP16 (Latency / FPS) | TensorRT C++ FP16 (Latency / FPS) |")
    print("| :--- | :--- | :--- | :--- |")
    for m_key in MODELS.keys():
        fp32_str = f"{speed_results[m_key]['FP32'][0]:.2f}ms / {speed_results[m_key]['FP32'][1]:.1f} FPS"
        fp16_str = f"{speed_results[m_key]['FP16'][0]:.2f}ms / {speed_results[m_key]['FP16'][1]:.1f} FPS"
        trt_str = f"{speed_results[m_key]['TRT_CPP'][0]:.2f}ms / {speed_results[m_key]['TRT_CPP'][1]:.1f} FPS"
        print(f"| {MODELS[m_key]['name']} | {fp32_str} | {fp16_str} | {trt_str} |")
        
    print("\n### DETECTION ACCURACY COMPARISON TABLE")
    print("| Model | Boar Video Detection Rate (%) | Waterdeer Video Detection Rate (%) |")
    print("| :--- | :--- | :--- |")
    for m_key in MODELS.keys():
        print(f"| {MODELS[m_key]['name']} | {accuracy_results[m_key]['boar']:.1f}% | {accuracy_results[m_key]['waterdeer']:.1f}% |")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()
