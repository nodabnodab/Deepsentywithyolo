#include <iostream>
#include <chrono>
#include <filesystem>
#include <vector>
#include <string>
#include <algorithm>
#include "detector.h"

namespace fs = std::filesystem;

const std::vector<std::string> COCO_CLASSES = {
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush"
};

const std::vector<std::string> CUSTOM_CLASSES = {
    "bear", "boar", "waterdeer", "human"
};

int main(int argc, char** argv) {
    // Default configuration
    std::string model_type = "best"; // default to custom model
    std::string input_dir = "/workspace/temp_frames";
    std::string output_dir = "/workspace/output_frames";
    
    if (argc > 1) {
        model_type = argv[1];
    }
    if (argc > 2) {
        input_dir = argv[2];
    }
    if (argc > 3) {
        output_dir = argv[3];
    }

    std::string engine_path;
    int num_classes = 0;
    const std::vector<std::string>* classes = nullptr;

    if (model_type == "best") {
        engine_path = "/workspace/best.engine";
        num_classes = 4;
        classes = &CUSTOM_CLASSES;
    } else if (model_type == "yolov11n") {
        engine_path = "/workspace/yolov11n.engine";
        num_classes = 80;
        classes = &COCO_CLASSES;
    } else if (model_type == "yolov8n") {
        engine_path = "/workspace/yolov8n.engine";
        num_classes = 80;
        classes = &COCO_CLASSES;
    } else {
        std::cerr << "Unknown model type: " << model_type << ". Use 'best', 'yolov11n', or 'yolov8n'." << std::endl;
        return -1;
    }

    std::cout << "=== Loading Engine: " << engine_path << " ===" << std::endl;
    std::cout << "=== Classes Count: " << num_classes << " ===" << std::endl;
    std::cout << "=== Frames Input Dir: " << input_dir << " ===" << std::endl;
    std::cout << "=== Frames Output Dir: " << output_dir << " ===" << std::endl;

    // Initialize Detector
    Detector detector(engine_path, num_classes, 0.25f, 0.45f);
    if (!detector.init()) {
        std::cerr << "Initialization failed for engine: " << engine_path << std::endl;
        return -1;
    }
    std::cout << "TensorRT engine loaded and GPU memory initialized successfully.\n" << std::endl;

    // Check input directory
    if (!fs::exists(input_dir)) {
        std::cerr << "Input directory does not exist: " << input_dir << std::endl;
        return -1;
    }

    // Collect all frame file paths
    std::vector<std::string> file_paths;
    for (const auto& entry : fs::directory_iterator(input_dir)) {
        std::string ext = entry.path().extension().string();
        std::transform(ext.begin(), ext.end(), ext.begin(), ::tolower);
        if (ext == ".jpg" || ext == ".jpeg" || ext == ".png") {
            file_paths.push_back(entry.path().string());
        }
    }
    
    if (file_paths.empty()) {
        std::cerr << "No image frames found in: " << input_dir << std::endl;
        return -1;
    }

    // Sort files alphabetically to preserve video frame order
    std::sort(file_paths.begin(), file_paths.end());
    std::cout << "Total frames found for processing: " << file_paths.size() << std::endl;

    // 1. Preload all frames into CPU memory to measure pure GPU inference/transfer speeds
    std::cout << "Preloading frames into memory..." << std::endl;
    std::vector<cv::Mat> frames;
    frames.reserve(file_paths.size());
    for (const auto& path : file_paths) {
        cv::Mat img = cv::imread(path);
        if (img.empty()) {
            std::cerr << "Failed to read image: " << path << std::endl;
            return -1;
        }
        frames.push_back(img);
    }
    std::cout << "Successfully preloaded " << frames.size() << " frames.\n" << std::endl;

    // 2. Perform Benchmarked Inference (isolated from disk read/write speeds)
    std::cout << "Running TensorRT inference benchmark..." << std::endl;
    std::vector<std::vector<Detection>> all_detections;
    all_detections.reserve(frames.size());

    auto start_time = std::chrono::high_resolution_clock::now();
    for (size_t i = 0; i < frames.size(); ++i) {
        all_detections.push_back(detector.detect(frames[i]));
    }
    auto end_time = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> total_inference_duration = end_time - start_time;
    double avg_latency = total_inference_duration.count() / frames.size();
    double avg_fps = 1000.0 / avg_latency;

    std::cout << "\n=== Inference Benchmark Complete ===" << std::endl;
    std::cout << "Total Frames Processed: " << frames.size() << std::endl;
    std::cout << "Total Inference Time: " << total_inference_duration.count() << " ms" << std::endl;
    std::cout << "Average Latency: " << avg_latency << " ms" << std::endl;
    std::cout << "Average Throughput: " << avg_fps << " FPS" << std::endl;

    // 3. Annotate and save the result frames to disk
    std::cout << "\nSaving annotated frames to disk..." << std::endl;
    fs::create_directories(output_dir);
    for (size_t i = 0; i < frames.size(); ++i) {
        cv::Mat annotated = frames[i].clone();
        for (const auto& det : all_detections[i]) {
            // Draw box
            cv::rectangle(annotated, det.box, cv::Scalar(0, 255, 0), 2);

            // Draw label
            std::string label = (*classes)[det.class_id] + ": " + cv::format("%.2f", det.confidence);
            int baseLine;
            cv::Size label_size = cv::getTextSize(label, cv::FONT_HERSHEY_SIMPLEX, 0.5, 1, &baseLine);
            
            int top = std::max(det.box.y, label_size.height);
            cv::rectangle(annotated, cv::Point(det.box.x, top - label_size.height),
                          cv::Point(det.box.x + label_size.width, top + baseLine),
                          cv::Scalar(0, 255, 0), cv::FILLED);
            cv::putText(annotated, label, cv::Point(det.box.x, top), cv::FONT_HERSHEY_SIMPLEX, 0.5, cv::Scalar(0, 0, 0), 1);
        }

        // Write to output directory with same file name
        std::string filename = fs::path(file_paths[i]).filename().string();
        std::string out_path = output_dir + "/" + filename;
        cv::imwrite(out_path, annotated);
    }
    std::cout << "All annotated frames saved successfully to: " << output_dir << std::endl;

    return 0;
}
