#include "utils.h"
#include <algorithm>
#include <numeric>

cv::Mat letterbox(const cv::Mat& src, cv::Size target_size, cv::Scalar pad_color, LetterboxInfo& info) {
    int src_w = src.cols;
    int src_h = src.rows;
    int target_w = target_size.width;
    int target_h = target_size.height;

    // Calculate scale factor
    float r = std::min((float)target_w / src_w, (float)target_h / src_h);
    int new_unpad_w = std::round(src_w * r);
    int new_unpad_h = std::round(src_h * r);

    // Calculate padding
    int dw = target_w - new_unpad_w;
    int dh = target_h - new_unpad_h;

    int pad_left = dw / 2;
    int pad_right = dw - pad_left;
    int pad_top = dh / 2;
    int pad_bottom = dh - pad_top;

    // Resize image
    cv::Mat resized;
    if (src_w != new_unpad_w || src_h != new_unpad_h) {
        cv::resize(src, resized, cv::Size(new_unpad_w, new_unpad_h), 0, 0, cv::INTER_LINEAR);
    } else {
        resized = src;
    }

    // Pad borders
    cv::Mat dst;
    cv::copyMakeBorder(resized, dst, pad_top, pad_bottom, pad_left, pad_right, cv::BORDER_CONSTANT, pad_color);

    // Store letterbox info for coordinate restoration
    info.scale = r;
    info.pad_w = pad_left;
    info.pad_h = pad_top;

    return dst;
}

void scale_boxes(cv::Rect& box, const LetterboxInfo& info, cv::Size original_size) {
    // Map bounding box coordinates back to the original size
    box.x = std::round((box.x - info.pad_w) / info.scale);
    box.y = std::round((box.y - info.pad_h) / info.scale);
    box.width = std::round(box.width / info.scale);
    box.height = std::round(box.height / info.scale);

    // Clip to original image boundaries
    box.x = std::max(0, std::min(box.x, original_size.width - 1));
    box.y = std::max(0, std::min(box.y, original_size.height - 1));
    box.width = std::max(0, std::min(box.width, original_size.width - box.x));
    box.height = std::max(0, std::min(box.height, original_size.height - box.y));
}

float calculate_iou(const cv::Rect& box1, const cv::Rect& box2) {
    int x1 = std::max(box1.x, box2.x);
    int y1 = std::max(box1.y, box2.y);
    int x2 = std::min(box1.x + box1.width, box2.x + box2.width);
    int y2 = std::min(box1.y + box1.height, box2.y + box2.height);

    int intersection_width = std::max(0, x2 - x1);
    int intersection_height = std::max(0, y2 - y1);
    float intersection_area = intersection_width * intersection_height;

    float union_area = box1.width * box1.height + box2.width * box2.height - intersection_area;
    if (union_area <= 0.0f) return 0.0f;
    return intersection_area / union_area;
}

void custom_nms(const std::vector<cv::Rect>& boxes, const std::vector<float>& confidences, const std::vector<int>& class_ids, float nms_threshold, std::vector<int>& indices) {
    std::vector<int> sorted_indices(boxes.size());
    std::iota(sorted_indices.begin(), sorted_indices.end(), 0);
    std::sort(sorted_indices.begin(), sorted_indices.end(), 
              [&confidences](int idx1, int idx2) {
                  return confidences[idx1] > confidences[idx2];
              });

    std::vector<bool> keep(boxes.size(), true);
    for (size_t i = 0; i < sorted_indices.size(); ++i) {
        int idx1 = sorted_indices[i];
        if (!keep[idx1]) continue;

        indices.push_back(idx1);

        for (size_t j = i + 1; j < sorted_indices.size(); ++j) {
            int idx2 = sorted_indices[j];
            if (!keep[idx2]) continue;

            // Class-specific NMS: only suppress if they belong to the same class
            if (class_ids[idx1] == class_ids[idx2]) {
                float iou = calculate_iou(boxes[idx1], boxes[idx2]);
                if (iou > nms_threshold) {
                    keep[idx2] = false;
                }
            }
        }
    }
}
