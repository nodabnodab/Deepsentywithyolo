# 🐾 야생동물 탐지 시스템 고도화 - 1단계 보고서

이미 학습이 완료된 커스텀 가중치 파일(`best.pt`)을 활용하여, 고성능 C++ 추론 환경 구축을 위한 **Docker 환경 셋업 및 TensorRT FP16 양자화 컴파일**을 완료했습니다.

---

## 💻 1. 개발 및 테스트 환경 (RTX 4070 Ti)

*   **Host OS:** Windows 11 (WSL2 Ubuntu 22.04 LTS)
*   **GPU:** NVIDIA GeForce RTX 4070 Ti (VRAM 12GB)
*   **Container:** NVIDIA NGC PyTorch Container (`nvcr.io/nvidia/pytorch:23.10-py3`)
*   **SW Version:** CUDA 12.2 / TensorRT 8.6.1 / PyTorch 2.1.0

---

## 🛠️ 2. 핵심 수행 작업

1.  **Docker & GPU 연동 검증:** WSL2와 Docker Desktop을 연동하고, 컨테이너 내부에서 Host GPU인 RTX 4070 Ti에 올바르게 가속 접근할 수 있도록 세팅을 마쳤습니다.
2.  **ONNX 익스포트:** PyTorch 가중치(`.pt`) 파일들을 플랫폼 독립적인 공통 규격인 `.onnx` 파일로 안전하게 변환했습니다. (opset=12, simplify 적용)
3.  **TensorRT FP16 양자화:** `trtexec` 도구를 사용하여 32비트 실수형(FP32) 가중치 파일들을 16비트 실수형(FP16) 반정밀도로 압축 및 컴파일하여 가속 엔진 파일(`.engine`)을 생성했습니다.

---

## 📊 3. 1단계 성능 비교 데이터 (trtexec 공식 벤치마크)

RTX 4070 Ti에서 FP16 양자화를 거친 TensorRT 엔진의 객관적인 추론 성능 수치입니다.

| 모델 명 (Model) | 변환 엔진 파일 (Engine File) | 처리 속도 (FPS) | 평균 지연 시간 (Latency) | 비고 |
| :--- | :--- | :--- | :--- | :--- |
| **YOLOv8n (순정)** | `yolov8n.engine` | **784.6 FPS** | **0.90 ms** | 속도 기준 비교군 |
| **YOLOv11n (순정)** | `yolov11n.engine` | **577.7 FPS** | **1.35 ms** | 아키텍처 기준 비교군 |
| **Custom Model (동물 3종)** | `best.engine` | **575.8 FPS** | **1.44 ms** | **본 프로젝트 핵심 모델** |

> 📌 **핵심 요약:** 1년 전 개발 완료된 커스텀 가중치(`best.pt`)를 성능 손실 없이 TensorRT FP16 양자화 엔진으로 변환하는 데 성공했습니다. RTX 4070 Ti 하드웨어 가속을 통해 프레임당 **1.44ms의 실시간 추론 속도(575 FPS)**를 확보했습니다.

---

## 📈 4. 모델별 추론 속도 비교 시각화 (그래프 영역)

*아래 영역은 3단계 벤치마크 프로그램 완성 후, 저장되는 이미지 그래프가 들어갈 자리입니다.*

```
[ 📊 1단계 컴파일 속도 비교 그래프 ]
┌────────────────────────────────────────────────────────┐
│  FPS (Higher is Better)                                │
│                                                        │
│  YOLOv8n (순정)    ████████████████████████████ 784 FPS│
│  YOLOv11n (순정)   ██████████████████ 577 FPS          │
│  best.engine (내것) ██████████████████ 575 FPS          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 5. 향후 진행 계획 (Next Steps)

*   **2단계:** CMake 및 OpenCV C++를 활용하여 컴파일 완료된 `best.engine`을 구동하는 **C++ 고성능 추론 Runner 프로젝트 구축**
*   **주요 기술:** C++ OpenCV, TensorRT C++ API, Pinned Memory & CUDA Stream 비동기 복사(Zero-Copy 효과 구현)
