import os
import sys

def export_model(model_path):
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found!")
        return False
    
    print(f"--- Exporting {model_path} to ONNX ---")
    try:
        from ultralytics import YOLO
        # Load model
        model = YOLO(model_path)
        # Export to ONNX with half=False (FP32 ONNX is standard, TensorRT will quantize to FP16)
        # We set dynamic=True for flexible batch/input size if needed, but static is usually faster in TensorRT.
        # Ultralytics default export usually works best.
        onnx_path = model.export(format="onnx", opset=12, simplify=True)
        print(f"Successfully exported {model_path} to {onnx_path}\n")
        return True
    except Exception as e:
        print(f"Failed to export {model_path}. Error: {e}\n")
        return False

if __name__ == "__main__":
    # Ensure ultralytics is installed
    try:
        import ultralytics
    except ImportError:
        print("Ultralytics library not found. Installing it now...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics"])
    
    # Models to export
    models_to_export = [
        "best.pt",
        "runs/train/weights/best.pt",
        "yolov11n.pt",
        "yolov8n.pt"
    ]
    
    for model in models_to_export:
        if os.path.exists(model):
            export_model(model)
        else:
            print(f"Skipping '{model}' (file does not exist).")
