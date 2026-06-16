#include "detector.h"
#include <fstream>

Detector::Detector(const std::string& engine_path, int num_classes, float conf_threshold, float nms_threshold)
    : engine_path_(engine_path), num_classes_(num_classes), conf_threshold_(conf_threshold), nms_threshold_(nms_threshold) {
    
    // Allocate CPU Pinned and GPU device memory sizes
    input_size_ = 1 * channels_ * input_w_ * input_h_ * sizeof(float);
    output_size_ = 1 * (4 + num_classes_) * num_anchors_ * sizeof(float);
}

Detector::~Detector() {
    // Release CUDA resources
    if (input_device_) cudaFree(input_device_);
    if (output_device_) cudaFree(output_device_);
    if (input_host_) cudaFreeHost(input_host_);
    if (output_host_) cudaFreeHost(output_host_);

    if (stream_) cudaStreamDestroy(stream_);

    // Release TensorRT resources
    if (context_) delete context_;
    if (engine_) delete engine_;
    if (runtime_) delete runtime_;
}

bool Detector::init() {
    // Load serialized TensorRT engine file
    std::ifstream file(engine_path_, std::ios::binary | std::ios::ate);
    if (!file.good()) {
        std::cerr << "Failed to open TensorRT engine file: " << engine_path_ << std::endl;
        return false;
    }

    size_t size = file.tellg();
    std::vector<char> engine_data(size);
    file.seekg(0, std::ios::beg);
    file.read(engine_data.data(), size);
    file.close();

    // Create runtime and deserialize engine
    runtime_ = nvinfer1::createInferRuntime(logger_);
    if (!runtime_) {
        std::cerr << "Failed to create IRuntime." << std::endl;
        return false;
    }

    engine_ = runtime_->deserializeCudaEngine(engine_data.data(), size);
    if (!engine_) {
        std::cerr << "Failed to deserialize CUDA engine." << std::endl;
        return false;
    }

    context_ = engine_->createExecutionContext();
    if (!context_) {
        std::cerr << "Failed to create IExecutionContext." << std::endl;
        return false;
    }

    // Allocate CPU Pinned Memory (Zero-Copy)
    cudaError_t status;
    status = cudaHostAlloc(reinterpret_cast<void**>(&input_host_), input_size_, cudaHostAllocDefault);
    if (status != cudaSuccess) {
        std::cerr << "Failed to allocate pinned CPU input memory: " << cudaGetErrorString(status) << std::endl;
        return false;
    }

    status = cudaHostAlloc(reinterpret_cast<void**>(&output_host_), output_size_, cudaHostAllocDefault);
    if (status != cudaSuccess) {
        std::cerr << "Failed to allocate pinned CPU output memory: " << cudaGetErrorString(status) << std::endl;
        return false;
    }

    // Allocate GPU Device Memory
    status = cudaMalloc(&input_device_, input_size_);
    if (status != cudaSuccess) {
        std::cerr << "Failed to allocate GPU device input memory: " << cudaGetErrorString(status) << std::endl;
        return false;
    }

    status = cudaMalloc(&output_device_, output_size_);
    if (status != cudaSuccess) {
        std::cerr << "Failed to allocate GPU device output memory: " << cudaGetErrorString(status) << std::endl;
        return false;
    }

    // Create CUDA Stream
    status = cudaStreamCreate(&stream_);
    if (status != cudaSuccess) {
        std::cerr << "Failed to create CUDA stream: " << cudaGetErrorString(status) << std::endl;
        return false;
    }

    return true;
}

void Detector::preprocess(const cv::Mat& frame, LetterboxInfo& info) {
    // 1. Perform letterboxing to keep aspect ratio
    cv::Mat letterboxed = letterbox(frame, cv::Size(input_w_, input_h_), cv::Scalar(114, 114, 114), info);

    // 2. Convert BGR to RGB and convert to float normalized to [0.0, 1.0]
    cv::Mat rgb;
    cv::cvtColor(letterboxed, rgb, cv::COLOR_BGR2RGB);
    rgb.convertTo(rgb, CV_32FC3, 1.0f / 255.0f);

    // 3. Convert HWC (Interleaved) to CHW (Planar) directly into CPU pinned memory
    std::vector<cv::Mat> channels;
    for (int i = 0; i < channels_; ++i) {
        channels.push_back(cv::Mat(input_h_, input_w_, CV_32FC1, input_host_ + i * input_h_ * input_w_));
    }
    cv::split(rgb, channels);
}

std::vector<Detection> Detector::detect(const cv::Mat& frame) {
    LetterboxInfo info;
    preprocess(frame, info);

    // Bindings array for enqueue
    void* bindings[] = {input_device_, output_device_};

    // 1. Async CPU -> GPU Copy
    cudaMemcpyAsync(input_device_, input_host_, input_size_, cudaMemcpyHostToDevice, stream_);

    // 2. Async Inference
    context_->enqueueV2(bindings, stream_, nullptr);

    // 3. Async GPU -> CPU Copy
    cudaMemcpyAsync(output_host_, output_device_, output_size_, cudaMemcpyDeviceToHost, stream_);

    // 4. Synchronize stream
    cudaStreamSynchronize(stream_);

    return postprocess(info, frame.cols, frame.rows);
}

std::vector<Detection> Detector::postprocess(const LetterboxInfo& info, int orig_w, int orig_h) {
    std::vector<cv::Rect> boxes;
    std::vector<float> confidences;
    std::vector<int> class_ids;

    // Transpose output from [1, 4 + num_classes, 8400] to extract predictions
    for (int i = 0; i < num_anchors_; ++i) {
        float max_score = 0.0f;
        int class_id = -1;

        // Find class with the maximum confidence score
        for (int c = 0; c < num_classes_; ++c) {
            float score = output_host_[(4 + c) * num_anchors_ + i];
            if (score > max_score) {
                max_score = score;
                class_id = c;
            }
        }

        // Filter out by confidence threshold
        if (max_score >= conf_threshold_) {
            float cx = output_host_[0 * num_anchors_ + i];
            float cy = output_host_[1 * num_anchors_ + i];
            float w  = output_host_[2 * num_anchors_ + i];
            float h  = output_host_[3 * num_anchors_ + i];

            // Convert center coordinates to bounding box top-left corner coordinates
            int x = std::round(cx - w / 2.0f);
            int y = std::round(cy - h / 2.0f);
            int width = std::round(w);
            int height = std::round(h);

            boxes.push_back(cv::Rect(x, y, width, height));
            confidences.push_back(max_score);
            class_ids.push_back(class_id);
        }
    }

    // Run Custom Non-Maximum Suppression (NMS)
    std::vector<int> indices;
    custom_nms(boxes, confidences, class_ids, nms_threshold_, indices);

    std::vector<Detection> detections;
    for (int idx : indices) {
        Detection det;
        det.class_id = class_ids[idx];
        det.confidence = confidences[idx];
        det.box = boxes[idx];

        // Scale box back to original input image size
        scale_boxes(det.box, info, cv::Size(orig_w, orig_h));
        detections.push_back(det);
    }

    return detections;
}
