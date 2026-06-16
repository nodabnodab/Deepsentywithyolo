#ifndef DETECTOR_H
#define DETECTOR_H

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <NvInfer.h>
#include <cuda_runtime_api.h>
#include <opencv2/opencv.hpp>
#include "utils.h"

class TensorRTLogger : public nvinfer1::ILogger {
public:
    void log(Severity severity, const char* msg) noexcept override {
        if (severity <= Severity::kWARNING) {
            std::cout << "[TensorRT] " << msg << std::endl;
        }
    }
};

class Detector {
public:
    Detector(const std::string& engine_path, int num_classes, float conf_threshold = 0.25f, float nms_threshold = 0.45f);
    ~Detector();

    bool init();
    std::vector<Detection> detect(const cv::Mat& frame);

private:
    std::string engine_path_;
    int num_classes_;
    float conf_threshold_;
    float nms_threshold_;

    TensorRTLogger logger_;
    nvinfer1::IRuntime* runtime_ = nullptr;
    nvinfer1::ICudaEngine* engine_ = nullptr;
    nvinfer1::IExecutionContext* context_ = nullptr;
    cudaStream_t stream_;

    // CPU Pinned Memory Buffers
    float* input_host_ = nullptr;
    float* output_host_ = nullptr;

    // GPU Device Memory Buffers
    void* input_device_ = nullptr;
    void* output_device_ = nullptr;

    size_t input_size_;
    size_t output_size_;

    int input_w_ = 640;
    int input_h_ = 640;
    int channels_ = 3;
    int num_anchors_ = 8400; // YOLOv8/v11 output boxes count

    void preprocess(const cv::Mat& frame, LetterboxInfo& info);
    std::vector<Detection> postprocess(const LetterboxInfo& info, int orig_w, int orig_h);
};

#endif // DETECTOR_H
