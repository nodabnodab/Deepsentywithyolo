# 야생동물 탐지 시스템 고도화 프로젝트 로드맵 (plan.md)

이 문서는 이미 학습이 완료된 커스텀 가중치 파일(`best.pt`)을 핵심으로 삼아, 이를 최적으로 구동하고 순정 YOLO 모델들과 성능을 객적으로 비교 분석할 수 있는 **고성능 C++ 추론 엔진 및 MLOps 환경 구축**을 위한 실행 계획입니다.

---

## 📅 프로젝트 목표 (Goal)
1.  **재학습 없음:** 수십 기가의 데이터셋이 없는 환경이므로, 이미 1년 전에 완성된 최종 커스텀 가중치(`best.pt`)를 그대로 사용합니다.
2.  **비교군 증명:** 순정 YOLO 모델(`yolov11n.pt`, `yolov8n.pt`)과 비교하여, 곰/멧돼지/고라니 탐지 시 커스텀 모델(`best.pt`)의 우수성(정확도 및 탐지 성공률)을 벤치마크 데이터로 입증합니다.
3.  **초고속 배포 파이프라인:** Docker 환경에서 TensorRT 엔진으로 컴파일하고 C++ 추론 파이프라인을 구축하여 프레임 레이터(FPS)를 극대화합니다.

---

## 📅 전체 개발 로드맵 (4단계)

```
[1단계: Docker 환경 구축 및 모델 컴파일]
  │ (best.pt, yolov11n.pt, yolov8n.pt 변환)
  ▼
[2단계: C++ 고성능 추론 엔진 구현]
  │ (OpenCV C++, TensorRT C++ API, Zero-Copy 적용)
  ▼
[3단계: Baseline 모델 비교 및 벤치마크 통계화]
  │ (blackbearsample.mp4 등 분석 및 오탐율/FPS 그래프 생성)
  ▼
[4단계: MLOps 기반 실시간 이벤트 로그 & 클라우드 연동]
  │ (Firebase 연동, 데이터 수집 루프 완성)
```

---

## 1단계: Docker 환경 구축 및 모델 컴파일 (Docker & TensorRT Setup)
*   **목표:** Native Windows 환경의 라이브러리 충돌 문제를 우회하기 위해 WSL2 Docker 개발 샌드박스를 만들고, 기존 가중치 파일들을 TensorRT 엔진으로 변환합니다.
*   **사용 기술:** Docker, WSL2, NVIDIA Container Toolkit, TensorRT (`trtexec`)
*   **상세 계획:**
    1.  **NVIDIA Docker 환경 구동:** WSL2 기반으로 NVIDIA Container Toolkit을 설치하여 Docker 내부에서 RTX 4070 Ti GPU에 가속 접근할 수 있도록 세팅합니다.
    2.  **NVIDIA NGC 컨테이너 실행:** CUDA, cuDNN, TensorRT가 이미 탑재된 공식 이미지를 로드하여 컨테이너 환경을 활성화합니다.
    3.  **3종 모델 TensorRT 변환:**
        *   비교 대상인 `yolov11n.pt`, `yolov8n.pt`와 커스텀 모델인 `best.pt`를 각각 `ONNX` 포맷으로 내보냅니다.
        *   컨테이너 내의 `trtexec`를 실행하여 3가지 모델을 RTX 4070 Ti에 최적화된 가속 엔진 파일(`.engine` 또는 `.trt`)로 컴파일합니다. (FP16 반정밀도 가속 적용)

---

## 2단계: C++ 고성능 추론 엔진 구현 (C++ Inference Runner)
*   **목표:** 파이썬의 속도 한계를 극복하기 위해, 컴파일된 TensorRT 엔진을 C++ 환경에서 다이렉트로 올려 돌리는 경량 엔진을 작성합니다.
*   **사용 기술:** C++, CMake, TensorRT C++ API, OpenCV C++
*   **상세 계획:**
    1.  **C++ 프로젝트 빌드 구성:** CMake를 사용하여 Docker 내에서 TensorRT C++ API 및 OpenCV가 정상 링크되도록 빌드 환경을 설정합니다.
    2.  **엔진 로드 및 메모리 바인딩:** C++ 코드로 `.engine` 파일을 역직렬화(Deserialize)하여 GPU에 올리고 입력/출력 텐서 주소를 바인딩합니다.
    3.  **Zero-Copy 및 멀티스레딩 설계:**
        *   카메라/동영상 프레임을 읽은 후 CPU 메모리에 올렸다가 GPU로 복사하는 과정을 최소화하기 위해, CUDA 스트림(`cudaMemcpyAsync`)을 활용하여 비동기식으로 GPU VRAM에 직배송하여 디바이스 내에서 처리를 완료합니다.
        *   영상 캡처와 추론 연산을 개별 스레드로 떼어내어 레이턴시를 최소화합니다.

---

## 3단계: Baseline 모델 비교 및 벤치마크 통계화 (Benchmarking)
*   **목표:** 순정 YOLO 모델들이 곰(`blackbearsample.mp4`), 고라니, 멧돼지 등을 감지하지 못하거나 엉뚱하게 감지(오탐)하는 한계를 정량적으로 밝히고, `best.pt`가 완벽하게 감지해냄을 통계 데이터로 증명합니다.
*   **사용 기술:** C++ 통계 로거, Matplotlib / Python Visualization
*   **상세 계획:**
    1.  **비교 추론 실행:** 준비된 테스트 비디오(`blackbearsample.mp4`, `boar_cam.mp4` 등)를 대상으로 `yolov11n.engine`, `yolov8n.engine`, `best.engine` 3가지를 각각 구동합니다.
    2.  **통계 데이터 추출:** 
        *   각 모델별 **객체 감지 신뢰도(Confidence Score) 추이**, **누락 프레임 수(Missed Frames)**, **프레임당 처리 시간(Latency, ms)**, **초당 프레임 수(FPS)**를 CSV 파일로 자동 로깅합니다.
    3.  **벤치마크 시각화:** 수집된 CSV 로그 데이터를 활용해 그래프를 그려 순정 모델의 오탐/미탐율 대비 커스텀 모델 `best.pt`가 가진 높은 정확도와 성능 우위를 포트폴리오용 통계 자료로 시각화합니다.

---

## 4단계: MLOps 기반 실시간 이벤트 로그 & 클라우드 연동 (MLOps & Cloud)
*   **목표:** C++ 엔진에서 탐지된 결과를 클라우드로 안전하게 전송하고 실시간으로 시각화할 수 있도록 연동 시스템을 구축합니다.
*   **사용 기술:** Firebase (Firestore, Storage), Python/C++ REST client
*   **상세 계획:**
    1.  **이벤트 녹화 파이프라인:** C++ 엔진이 구동되면서 동물이 2초 이상 감지되는 이벤트가 발생하면, 앞뒤 8~10초 분량의 영상을 클립으로 추출합니다.
    2.  **Firebase 업로드 자동화:** 추출된 영상 파일은 Firebase Storage에 업로드하고, 탐지 시각, 동물 종류, 위치 등의 텍스트 로그는 Firestore DB에 비동기식으로 기록합니다.
    3.  **액티브 러닝용 수집 환경 마련:** 모델의 판단이 모호한 구간(Confidence 0.4 ~ 0.6)의 프레임 이미지들만 따로 필터링하여 Firebase Storage의 `unlabeled/` 경로에 분류 수집하는 파이프라인을 갖추어 차세대 데이터 파이프라인의 기반을 닦습니다.
