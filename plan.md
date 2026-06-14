# 야생동물 탐지 시스템 고도화 프로젝트 로드맵 (plan.md)

이 문서는 AI 모델 구조 개선(SOTA Attention), C++ 및 TensorRT 기반 경량화 최적화, 그리고 MLOps 피드백 루프 구축을 유기적으로 연결하여 실제 상용화 가능한 수준의 컴퓨터 비전 시스템을 구축하기 위한 상세 실행 계획입니다.

---

## 📅 전체 개발 로드맵 (4단계)

```
[1단계: Baseline 및 데이터 가공] ──> [2단계: EMA Attention 모델 커스텀] 
                                                    │ (4번째 P5 단계 적용)
                                                    ▼
[4단계: MLOps Active Learning 루프] <── [3단계: C++ TensorRT 최적화]
```

---

## 1단계: 데이터 전처리 및 환경 검증 (Baseline Setup)
*   **목표:** 본격적인 모델 개량 전에 기준점(Baseline)이 되는 데이터셋을 정제하고 기본 학습 환경을 완벽하게 검증합니다.
*   **주요 기술:** Python, PyTorch, Ultralytics YOLOv11, Labelme
*   **상세 계획:**
    1.  **데이터셋 정제:** `PolyProject/animal/`에 존재하는 원본 데이터(Bear, Boar, Waterdeer)의 라벨 결측치 및 이미지 오류를 검사합니다.
    2.  **재현 가능한 Train/Val 분할:** 난수 시드(Seed=42)를 고정하여 항상 동일하게 분할되는 데이터 가공 스크립트를 최종 실행합니다.
    3.  **Baseline 학습:** 순정 YOLOv11n(nano) 모델을 커스텀 데이터셋으로 25에폭 동안 학습하여 기준 mAP50-95 및 추론 FPS 값을 기록합니다. (비교군 확보)

---

## 2단계: 최신 논문(EMA) 기반 모델 커스터마이징 (Model Design)
*   **목표:** 최신 SOTA(State-of-the-Art) Attention 논문을 분석하고, YOLOv11 백본의 4번째 단계에 모듈을 직접 코드로 구현하여 삽입한 뒤 성능을 비교합니다.
*   **주요 기술:** Python, PyTorch, YOLOv11 Custom Architecture (YAML)
*   **백본의 4가지 단계 및 EMA 삽입 위치 결정:**
    *   YOLO 백본은 특징 맵을 축소해 나가며 4개의 메인 다운샘플링 블록(C3k2/C2f)을 거칩니다:
        1.  **1번째 단계 (P2 / $160 \times 160$):** 저수준의 윤곽선 정보 위주. Attention 연산량이 너무 커 속도 저하가 심함.
        2.  **2번째 단계 (P3 / $80 \times 80$):** 작은 동물 탐지용.
        3.  **3번째 단계 (P4 / $40 \times 40$):** 중간 크기 동물 탐지용.
        4.  **4번째 단계 (P5 / $20 \times 20$):** 가장 추상적이고 고차원적인 문맥(Semantic) 정보가 모이는 곳. 
    *   **결정:** **4번째 단계 (P5 블록 바로 뒤, SPPF 직전)**에 EMA를 적용합니다. 해상도가 가장 작아 **TensorRT 변환 시 속도(FPS) 저하가 가장 적으면서도, 고차원적 인식력을 극대화**할 수 있기 때문입니다.

### 📄 4번째 단계에 반영할 핵심 논문 출처 및 기술 분석

*   **논문 출처:**
    *   **제목:** *Efficient Multi-Scale Attention Module with Cross-Spatial Learning* (ICASSP 2023)
    *   **저자:** Dali Zhang, Chaishuang Lin, Jiashuai Li, et al.
    *   **아카이브 링크:** [arXiv:2305.13563](https://arxiv.org/abs/2305.13563)
    *   **공식 코드 저장소:** [GitHub - YOLOonMe/EMA-attention-module](https://github.com/YOLOonMe/EMA-attention-module)

*   **논문 핵심 기술 원리 (EMA 모듈):**
    1.  **채널 그룹화 (Sub-feature Grouping):** 기존 SE, CBAM 등은 채널 수 조절 시 차원 축소를 하여 정보 소실이 일어났으나, EMA는 채널을 여러 그룹으로 나누어 다양한 스케일의 특징 정보가 독립적으로 살아있게 보존합니다.
    2.  **병렬 분기 처리 (Parallel Branches):** 두 개의 1D Average Pooling 분기와 하나의 3x3 Conv 분기를 병렬로 구동하여 전역적(Global)인 문맥 정보와 국소적(Local)인 위치 정보를 동시에 추출합니다.
    3.  **크로스 공간 학습 (Cross-Spatial Learning):** 분기별로 나온 가중치 행렬을 곱하거나 연산할 때 차원을 변형(Reshape & Permute)하여 공간 정보를 서로 교차 피드백(Cross-Dimension Interaction)시킵니다. 이를 통해 수풀 뒤에 숨겨진 동물의 특징을 3차원적(Channel, Height, Width)으로 복합 분석합니다.

---

## 3단계: Docker 환경 및 TensorRT 기반 C++ 초고속 추론 엔진 구현

*   **목표:** Native Windows의 복잡한 패키지 의존성 문제를 해결하기 위해 Docker(WSL2) 환경을 선구축하고, 모델을 TensorRT로 최적화 컴파일한 뒤, 최종 C++ 실시간 영상 추론 엔진을 완성합니다.
*   **이상적인 개발 순서:** **[3-1. Docker 환경 구축] ➡️ [3-2. TensorRT 컴파일] ➡️ [3-3. C++ 추론 엔진 작성]**

### 3-1. Docker 개발 환경 구축 (WSL2 & NVIDIA Container)
*   **사용 기술:** Windows Subsystem for Linux 2 (WSL2), Docker Desktop, NVIDIA Container Toolkit, NVIDIA NGC PyTorch Container
*   **상세 계획:**
    1.  **WSL2 백엔드 및 Docker 활성화:** Windows에서 Linux 배포판을 구동하고 Docker Desktop과 연동합니다.
    2.  **NVIDIA Container Toolkit 설치:** WSL2 내부의 Docker 컨테이너가 윈도우 호스트의 RTX 4070 Ti GPU에 직접 접근할 수 있도록 드라이버 통로를 연결합니다.
    3.  **NVIDIA NGC 컨테이너 실행:** CUDA, cuDNN, TensorRT, PyTorch가 완벽하게 세팅되어 검증된 NVIDIA 공식 이미지(`nvcr.io/nvidia/pytorch` 등)를 다운로드(Pull)하고 실행하여 개발 샌드박스를 완성합니다.

### 3-2. SOTA 모델의 TensorRT 최적화 컴파일 (ONNX ➡️ Engine)
*   **사용 기술:** PyTorch ONNX exporter, TensorRT `trtexec` compiler
*   **상세 계획:**
    1.  **ONNX 파일 내보내기:** 2단계에서 완성한 `YOLOv11-EMA` 모델(`best.pt`)을 Docker 환경 내에서 공용 번역 포맷인 `.onnx` 파일로 내보냅니다.
    2.  **가속 엔진 컴파일:** TensorRT에서 제공하는 모델 컴파일러 도구인 `trtexec`를 실행합니다.
        *   RTX 4070 Ti GPU 아키텍처에 맞게 레이어를 병합(Layer Fusion)하고 최적화 메모리를 할당합니다.
        *   **FP16(반정밀도) 연산 활성화:** 4070 Ti의 Tensor Core를 극대화 활용하기 위해 반정밀도 연산을 적용하여 정확도 손실을 최소화하면서 추론 속도를 배가시킵니다.
        *   최종 직렬화된 가속 모델 파일인 `yolo11_ema.engine`(또는 `.trt`)을 생성합니다.

### 3-3. 고성능 C++ 추론 엔진 개발 (Inference Runner)
*   **사용 기술:** C++, CMake, TensorRT C++ API, OpenCV C++
*   **상세 계획:**
    1.  **C++ 빌드 환경 구성:** Docker 컨테이너 내에서 CMake를 이용해 TensorRT 및 OpenCV 라이브러리가 올바르게 링크되도록 빌드 파일을 정의합니다.
    2.  **TensorRT 엔진 로드 및 실행:** C++ 코드로 `.engine` 파일을 읽어 GPU 메모리에 모델을 올리고(Deserialization), 입출력 버퍼(Tensor Bindings)를 할당합니다.
    3.  **Zero-Copy 기법 적용:**
        *   OpenCV C++로 카메라/동영상 프레임을 읽어옵니다.
        *   프레임 데이터를 CPU 메모리(RAM)를 거쳐 복사하는 횟수를 제로(0)로 만들기 위해, CUDA의 비동기 메모리 복사(`cudaMemcpyAsync`) 및 스트림(CUDA Streams) 제어를 통해 GPU 디바이스 메모리로 즉각 다이렉트 바인딩 처리를 수행합니다.
    4.  **멀티스레드 비동기 설계:** 프레임 캡처 스레드와 TensorRT 추론 스레드를 분리하여 프레임 드랍이나 딜레이 없는 실시간 추론을 보장합니다.

---

## 4단계: MLOps 기반 Active Learning 피드백 루프 구축 (MLOps Active Learning)
*   **목표:** 현장 장비(C++ 추론기)와 서버(Firebase)를 연결하여 모델 성능 저하를 방지하고 주기적으로 모델이 스스로 똑똑해지는 오답노트 시스템을 구축합니다.
*   **주요 기술:** Python automation, Firebase (Firestore, Storage), REST API
*   **상세 계획:**
    1.  **경계치 데이터 추출 필터 설계:** C++ 추론 엔진에서 객체를 검출할 때, 예측 신뢰도(Confidence Score)가 `0.4 ~ 0.6` 사이인 "판단하기 애매한 프레임"을 필터링하여 선별 보관합니다.
    2.  **자동 업로드:** 선별된 이미지를 백그라운드 스레드를 통해 Firebase Storage로 자동 저장하고 Firestore에 업로드 로그를 남깁니다.
    3.  **자동 재학습(Retraining) 트리거:**
        *   Firebase Storage에 오답노트 데이터가 일정 갯수 이상 쌓이면 알림 또는 트리거를 발생시킵니다.
        *   수집된 데이터에 라벨을 주입한 뒤, 기존 1단계에서 완성했던 `YOLOv11-EMA` 모델의 가중치를 바탕으로 자동 점진적 재학습(Incremental Learning)을 트리거하는 MLOps 자동화 스크립트를 완성합니다.
