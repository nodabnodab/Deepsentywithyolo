# 🐾 야생동물 탐지 시스템 고도화 - 1~3단계 통합 기술 보고서

본 보고서는 이미 학습 완료된 커스텀 가중치 파일(`best.pt`)을 활용하여 **Docker 환경 셋업, TensorRT 컴파일, C++ 비동기 추론 파이프라인 개발, 그리고 순정 YOLO 모델들과의 성능/정확도 비교 벤치마크**를 수행한 결과를 정리한 포트폴리오 문서입니다.

---

## 💻 1. 개발 및 검증 환경 (RTX 4070 Ti)

*   **Host OS:** Windows 11 (WSL2 Ubuntu 22.04 LTS)
*   **GPU:** NVIDIA GeForce RTX 4070 Ti (VRAM 12GB)
*   **Container:** NVIDIA NGC PyTorch Container (`nvcr.io/nvidia/pytorch:23.10-py3`)
*   **SW Version:** CUDA 12.2 / TensorRT 8.6.1 / PyTorch 2.1.0 / OpenCV 4.7.0 (NGC 빌드)

---

## 🛠️ 2. 핵심 수행 작업 요약

### [1단계] Docker 환경 구축 및 TensorRT 컴파일
*   WSL2 환경 하에서 NVIDIA Container Toolkit을 활성화하여 GPU 가속 컨테이너를 가동했습니다.
*   `best.pt`, `yolov8n.pt`, `yolov11n.pt` 모델을 `ONNX`로 내보내고 `trtexec`를 사용해 RTX 4070 Ti에 최적화된 **TensorRT FP16 가속 엔진 파일(`.engine`)**로 컴파일했습니다.

### [2단계] C++ 고성능 추론 엔진 구현
*   **C++ 기반 고속 런타임 최적화:** PyTorch Python의 런타임 오버헤드를 모두 걷어내기 위해 **C++ 기반 TensorRT 추론 러너**를 구현했습니다.
*   **Pinned Memory & Zero-Copy 효과 구현:** `cudaHostAlloc`로 CPU Page-locked (Pinned) Memory를 직접 확보하고, BGR ➡️ CHW 평면 분할 작업(`cv::split`)을 해당 메모리에 다이렉트로 매핑했습니다. 이를 통해 CPU 블로킹을 차단하고, CUDA 스트림(`cudaMemcpyAsync`) 기반의 비동기 DMA(Direct Memory Access) 전송을 실행하여 PC 환경에서의 Zero-Copy 전송 효과를 완벽히 구현했습니다.
    *   *💡 외장 GPU(PC)와 Jetson의 차이점 반영:* 통합 메모리(Unified Memory)를 쓰는 Jetson과 달리 외장 GPU(RTX 4070 Ti) 환경에서는 물리적 메모리가 분리되어 있습니다. 따라서 GPU가 호스트 메모리를 실시간으로 매번 읽는 Mapped Zero-Copy 대신, Pinned Memory 버퍼와 비동기 DMA 복사를 연동하여 고속 VRAM(GDDR6X)으로 전송한 후 연산하는 구조가 처리량(Throughput) 극대화에 훨씬 유리하므로 이 설계를 채택했습니다.
*   **커스텀 클래스별 NMS(Class-Specific NMS) 구현:** 컨테이너 내의 OpenCV가 DNN 모듈 누락으로 빌드된 제약을 극복하기 위해, 이중 검출 박스 억제(IoU 계산) 로직을 C++로 자체 직접 작성하여 완벽하게 구동시켰습니다.

### [3단계] Baseline 모델 성능/정확도 정량적 비교 검증
*   동영상 프레임을 미리 RAM에 올린 후 연산하여 디스크 I/O 병목을 제거한 상태에서 PyTorch Python(FP32/FP16)과 C++ TensorRT(FP16) 간의 처리량(FPS) 및 지연 속도(Latency)를 정밀하게 계측했습니다.
*   멧돼지(boar) 및 고라니(waterdeer) 비디오를 활용하여 순정 COCO 모델의 클래스 식별 부재 한계를 정량적으로 밝히고 커스텀 모델의 우수성을 정량 수치로 산출했습니다.

---

## 📊 3. 추론 속도 및 지연 시간 벤치마크 결과

실제 디스크 I/O 병목이 배제된 상태에서 300 프레임 기준으로 계측한 통합 속도 데이터입니다.

### ⚡ 3종 모델의 런타임별 속도 비교 표
| 모델 명 (Model) | Python PyTorch FP32 (Latency / FPS) | Python PyTorch FP16 (Latency / FPS) | TensorRT C++ FP16 (Latency / FPS) |
| :--- | :--- | :--- | :--- |
| **Custom Model (best.pt)** | 9.83 ms / 101.7 FPS | 9.80 ms / 102.1 FPS | **2.79 ms / 358.7 FPS** |
| **Pure YOLOv8n** | 9.11 ms / 109.8 FPS | 10.63 ms / 94.1 FPS | 4.00 ms / 250.0 FPS |
| **Pure YOLOv11n** | 10.75 ms / 93.1 FPS | 11.69 ms / 85.6 FPS | 4.33 ms / 230.7 FPS |

> 💡 **벤치마크 분석 결과:**
> *   **파이썬 대비 3.5배 ~ 4배 속도 개선:** 파이썬 PyTorch 환경 대비 C++ TensorRT FP16 추론 엔진은 지연 시간을 약 **2.79ms** 수준으로 단축시켰으며, 속도는 **358 FPS**로 폭증했습니다.
> *   **클래스 개수 최적화 효과:** 순정 YOLOv8/v11 모델(COCO 80개 클래스)에 비해 커스텀 모델(4개 클래스)은 후처리(Transposition 및 NMS 루프) 연산량이 감소하여 C++ 추론 파이프라인에서 순정 모델(230~250 FPS)보다 **약 100 FPS 이상 빠른 속도**를 뿜어냈습니다.

### 📈 처리량 및 지연 시간 시각화 그래프
![Inference Throughput Comparison](./inference_results/throughput_fps.png)
![Inference Latency Comparison](./inference_results/latency_ms.png)

---

## 🎯 4. 야생동물 탐지 성공률 비교 결과

순정 COCO 모델에는 한국 농가와 산간 지역에서 핵심 유해조수로 분류되는 **멧돼지(boar)** 및 **고라니(waterdeer)** 클래스가 존재하지 않습니다. 이를 증명하기 위해 실제 동물 비디오의 각 300프레임 구간에서 정상 감지 여부를 테스트했습니다.

### 🦌 야생동물 탐지 성공률 비교 표
| 모델 명 (Model) | 멧돼지 비디오 올바른 탐지율 (%) | 고라니 비디오 올바른 탐지율 (%) |
| :--- | :--- | :--- |
| **Custom Model (best.pt)** | **15.7%** | **34.7%** |
| **Pure YOLOv8n (COCO)** | 0.0% (오탐/미탐) | 0.0% (오탐/미탐) |
| **Pure YOLOv11n (COCO)** | 0.0% (오탐/미탐) | 0.0% (오탐/미탐) |

> 📌 **핵심 결과:**
> 순정 YOLO 모델들은 멧돼지나 고라니가 출현했을 때 감지를 전혀 하지 못하거나 개(dog), 양(sheep), 소(cow) 등 엉뚱한 가축으로 식별하여 야생 조수 피해 방지 시스템으로서는 사용이 완전히 불가능했습니다. 
> 반면, 커스텀 모델은 1 epoch의 가벼운 학습만 진행되었음에도 불구하고 멧돼지와 고라니를 **정확한 클래스 ID로 매핑하여 탐지해 냄**을 증명했습니다.

### 📈 야생동물 탐지 성공률 시각화 그래프
![Wildlife Detection Success Rate Comparison](./inference_results/detection_accuracy.png)

---

## 🚀 5. 향후 진행 계획 (Phase 4)

*   **4단계: Firebase MLOps 연동 및 실시간 이벤트 로깅**
    *   C++ 추론 엔진에서 유해 야생동물이 일정 임계 시간(예: 2초) 동안 지속 검출될 시, 이벤트 영상 클립을 FFmpeg으로 즉각 슬라이싱합니다.
    *   생성된 이벤트 영상 클립은 Firebase Storage에, 탐지 시간, 객체 종류, 신뢰도 등 텍스트 로그는 Firestore DB에 비동기식으로 실시간 전송/기록하여 원격 관리 및 데이터 축적이 가능한 MLOps 환경을 구축할 예정입니다.
