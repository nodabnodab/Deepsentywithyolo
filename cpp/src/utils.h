#ifndef UTILS_H
#define UTILS_H

#include <opencv2/opencv.hpp>
#include <vector>

struct LetterboxInfo {
    float scale;
    int pad_w;
    int pad_h;
};

struct Detection {
    int class_id;
    float confidence;
    cv::Rect box;
};

// Letterbox pre-processing: maintains image aspect ratio and pads borders.
cv::Mat letterbox(const cv::Mat& src, cv::Size target_size, cv::Scalar pad_color, LetterboxInfo& info);

// Scales bounding box coordinates back to original image size.
void scale_boxes(cv::Rect& box, const LetterboxInfo& info, cv::Size original_size);

// Custom Class-Specific Non-Maximum Suppression (NMS) since OpenCV DNN is missing.
void custom_nms(const std::vector<cv::Rect>& boxes, const std::vector<float>& confidences, const std::vector<int>& class_ids, float nms_threshold, std::vector<int>& indices);

#endif // UTILS_H
