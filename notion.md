🛠 기술 스택 (Tech Stack)
AI & Vision: Python, YOLOv11, OpenCV, Scikit-learn
Backend (Database): Firebase Firestore Database, Firebase Storage
Mobile App: C#, .NET MAUI
Tools & Environment: Visual Studio Code, Virtual Environments

# 성과

## ***2025 제5회 전국 대학교 이그나이트 스토리텔링 경진대회 장려상 수상**

!image.png

커스텀 모델과 YOLOv11 비교

!image.png

!image.png

# 프로젝트 개요

이 시스템은 AI 객체 인식 기반의 YOLO 모델을 활용하여 유해야생동물을 실시간으로 탐지하고 대응하는 기술을 제공합니다. YOLO로 탐지된 정보를 시각화하고 실시간 경고를 제공하는 모바일 애플리케이션을 직접 개발하여, 사용자가 현장 상황을 즉각적으로 파악하고 신속하게 대응할 수 있도록 지원했습니다. 이를 통해 농작물 피해를 최소화하고, 효율적인 관리 및 경고 서비스를 제공함으로써 농업 현장의 안전성과 생산성을 높이는 것이 본 프로젝트의 핵심 목표입니다.

# 시연 영상

https://youtu.be/_SldaSuC09s

# 기술 스택

### ✅ S/W_모바일 어플리케이션

- `C#`
- `XAML`
- `Visual Studio 2022`
- `.NET MAUI(net 8.0)`
- `Microcharts(1.0.0)`
- `SkiaSharp(2.88.3)`
- `MediaElement(4.1.2)`

### ✅ S/W_Yolo 객체 인식

- `VS Code`
- `YOLOv11`
- `Labelme2yolo`
- `OpenCV`
- `Scikit-learn`
- `기타 : uuid, threading`

---

### ✅ DB

- `Firebase_FireStore Database`
- `Firebase_Storage`

### ✅ OS / Tools

- `Windows11`
- `Drow.io`

---

### **기술 선정 이유**

✅ YOLOv11 (Python)

프로젝트 초기에는 하드웨어 기반의 실시간 객체 인식 시스템을 구축하기 위해 YOLOv4 기반의 경량화 모델을 설계하였습니다. 그러나 Jetson Nano 등 엣지 디바이스를 활용하기 위한 하드웨어 재료 수급 일정에 차질이 발생하였고, 이에 따라 최신 모델인 YOLOv11을 기반으로 우선 소프트웨어 프로토타입을 구현하였습니다. 웹캠을 활용한 실시간 탐지 시스템을 구축하여 개발 일정을 준수하면서도 주요 기능을 검증할 수 있었습니다. 

- **단일 단계 검출 기반의 실시간성**
RCNN 계열에 비해 구조가 단순하고 처리 속도가 빨라, 실시간 객체 감지에 최적화된 YOLO 아키텍처 사용
- **최신 모델 기반의 탐지 정확도**
YOLOv11의 향상된 알고리즘과 학습 성능을 통해 야생동물 탐지 정확도 및 신뢰도 확보
- **시스템 연동성과 확장성**
Firebase와의 원활한 연동을 통해 모바일 앱에 탐지 결과를 실시간 제공할 수 있으며, 모듈화된 구조로 기능 확장이 용이함

✅ .NET MAUI (C# & XAML)

모바일 애플리케이션 구현을 위해 다양한 프레임워크(.NET MAUI, Flutter, React Native)를 비교·검토한 결과, 최종적으로 .NET MAUI를 채택하게 된 이유는 다음과 같습니다.

1. **기존 개발 경험의 연속성**
C# 개발 경험이 있었기 때문에, 개발 경험이 없는 Dart나 Java보다 학습에 소요되는 시간이 현저히 낮고, 빠르게 개발에 착수할 수 있었음
2. **크로스 플랫폼 빌드 지원**
하나의 코드베이스로 Android 및 iOS 앱을 동시에 개발 가능해 리소스를 효율적으로 활용할 수 있었음
3. **UI/UX 구현의 익숙함(마크업 언어 기반의 구조로 학습 용이)**
 XAML은 CSS, JavaScript 등 웹 개발에 자주 사용되는 마크업 언어와 유사한 구조를 가져 직관적으로 학습 및 적용 가능
4. **Firebase 연동 용이성**
HTTPClient 기반의 REST API 연동이 가능하며, Firebase와의 통합이 수월하여 실시간 데이터 반영 및 알림 기능 구현에 효과적
5. **기술자료는 적었지만, 문제 해결 가능성 확보**
참고할 수 있는 자료는 제한적이었지만, Microsoft 공식 문서 및 커뮤니티가 존재하고, 기존 C# 기반의 개발 경험을 토대로 학습과 구현을 병행

✅ Firebase (DB)
DB 구축과정에서 SQL Server, SQL Lite, Firebase 등 다양한 모델이 논의되었습니다. 그중 Firebase를 선정한 사유는 다음과 같습니다.

1. **클라우드 기반 아키텍처**
별도의 서버 구축 및 유지보수가 필요 없고, 실시간 데이터 동기화가 가능하여 실시간 모니터링에 최적화된 환경 제공
2. **다양한 SDK 및 개발 환경과의 호환성**  
Python과 MAUI(C#, XAML) 등 본 프로젝트의 주요 개발 스택과 높은 호환성을 지닌 SDK 및 라이브러리 제공
3. **정형 및 비정형 데이터의 효율적 처리**  
탐지 로그(정형 데이터)와 탐지 영상(비정형 데이터) 등 다양한 형식의 데이터 저장 및 관리가 용이
4. **NoSQL 기반의 경량화된 데이터 처리 모델**  
스키마 유연성과 빠른 처리 속도 덕분에, 유해야생동물 탐지와 같은 이벤트 중심의 프로젝트 성격에 적합

# 프로젝트 설계

### 아키텍처 구조

!image.png

### 스토리보드 / 화면설계서

!초안

초안

!목업 이미지

목업 이미지

### FlowChart

1. 처리부_Yolo11 객체 인식
    
    !image.png
    
2. DB
    
    !image.png
    
3. 구동부_모바일 어플리케이션

!app_flowchart.drawio (1).png.png)

# 주요 기능

✅ 처리부_Label 데이터 가공

- 데이터 표준화 진행 : 공공데이터 json 포맷 데이터를 LabelIMe 포맷으로 일괄 변환
    - 코드
        
        ```python
        import os
        import json
        import base64
        
        source_json_dir = 'C:\\Users\\AREU\\Desktop\\PolyProject\\animal\\onlyfew\\validation\\waterdeer'
        # 원본 JSON 파일이 저장된 경로
        
        image_dir = 'C:\\Users\\AREU\\Desktop\\PolyProject\\animal\\onlyfew\\validation\\waterdeer'
        # 이미지 파일이 저장된 경로 (반드시 실제 경로로 수정해야함!)
        
        output_dir = 'C:\\Users\\AREU\\Desktop\\PolyProject\\animal\\onlyfew\\validation\\waterdeer_export'
        # 변환된 JSON 파일을 저장할 경로
        
        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # JSON 파일 탐색
        json_paths = []
        for filename in os.listdir(source_json_dir):
            if os.path.splitext(filename)[1].lower() == '.json':
                json_paths.append(os.path.join(source_json_dir, filename))
        
        # 각 JSON 파일 처리
        for json_file in json_paths:
            # JSON 파일 읽기
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        
            # LabelMe 형식 초기화
            main_group = {}
            main_group['version'] = "4.5.6"
            main_group['flags'] = {}
            main_group['shapes'] = []
        
            # 이미지 정보 추출 및 설정
            image_info = json_data['images'][0]  # 첫 번째 이미지 정보 사용
            main_group['imagePath'] = image_info['file_name']  # 이미지 파일명
            main_group['imageHeight'] = image_info['height']   # 이미지 높이
            main_group['imageWidth'] = image_info['width']     # 이미지 너비
        
            # 이미지 데이터 미포함 (주석 처리 및 명시적 설정)
            main_group['imageData'] = None  # 이미지 데이터 미포함
        
            # 어노테이션 정보 변환, 주석 달기 위해 한번 ctrl cv 함. 오류 발생 가능성 약간 있으니 주의
        
        ###########
            # 이미지 안에 있는 각 객체(어노테이션) 정보를 하나씩 순회....
            for annotation in json_data['annotations']:
                
                # LabelMe의 'shapes' 리스트에 들어갈 새로운 딕셔너리(객체 정보)를 생성.
                gr = {} 
                
                # 'category_name' 값을 가져와 객체의 이름(예: 'boar')을 'label' 키에 저장.
                gr['label'] = annotation['category_name']
                
                # 1. Bounding Box(사각형) 정보가 있는지 확인.
                # 가장 우선적으로 처리할 어노테이션 유형.
                if annotation['bbox'] is not None:
                    
                    # LabelMe 형식에 맞게 'points' 키에 좌상단, 우하단 좌표 리스트를 저장.
                    gr['points'] = [
                        [annotation['bbox'][0][0], annotation['bbox'][0][1]],
                        [annotation['bbox'][1][0], annotation['bbox'][1][1]]
                    ]
                    
                    # 이 객체의 모양이 '사각형'임을 명시.
                    gr['shape_type'] = 'rectangle'
                    
                # 2. Bounding Box 정보는 없지만, Segmentation(폴리곤) 정보가 있는지 확인.
                elif annotation['segmentation'] is not None:
                    
                    # segmentation은 [x1, y1, x2, y2, ...] 형태로 된 긴 리스트입니다.
                    points = annotation['segmentation'][0]
                    
                    # 이 리스트를 [[x1, y1], [x2, y2], ...] 형태의 좌표 쌍 리스트로 변환하여 'points'에 저장합니다.
                    gr['points'] = [[x, y] for x, y in zip(points[::2], points[1::2])]
                    
                    # 이 객체의 모양이 '다각형'임을 명시합니다.
                    gr['shape_type'] = 'polygon'
                    
                # 3. Bbox와 Segmentation 정보가 모두 없는 비정상적인 데이터의 경우,
                else:
                    # 오류 메시지를 출력하고, 이 어노테이션은 무시하고 다음 어노테이션으로 넘어갑니다. (continue)
                    print(f"bbox와 segmentation 모두 없음: {json_file}, annotation id: {annotation['id']}")
                    continue
        
                # LabelMe 형식에 필요한 추가적인 키들을 기본값으로 설정합니다.
                gr['group_id'] = None
                gr['flags'] = {}
        
                # 완성된 객체 정보(gr)를 최종 결과물(main_group)의 'shapes' 리스트에 추가합니다.
                main_group['shapes'].append(gr) 
        
            # 변환된 JSON 파일 저장
            output_file = os.path.join(output_dir, os.path.basename(json_file))  # 출력 파일명 동적 생성
            with open(output_file, 'w', encoding='utf-8') as make_file:
                json.dump(main_group, make_file, indent="\t", ensure_ascii=False)
        
            print(f"변환 완료: {output_file}")
        ```
        
- YOLO 포맷 변환 : 데이터 표준화를 거친 후 최종적으로 YOLO 학습이 가능한 포맷으로 변환
    - 코드
        
        ```python
        import os
        import json
        import shutil
        import random
        from pathlib import Path
        
        def convert_labelme_to_yolo(base_dir, train_ratio=0.8):
            """
            LabelMe JSON 파일들을 YOLO 형식으로 변환
            train/val 비율을 조정하여 데이터를 나눔
            """
            
            # 클래스 매핑 정의
            class_mapping = {
                'thibetanus': 0,  # bear
                'scrofa': 1,      # boar  
                'inermis': 2      # waterdeer
            }
            
            # 출력 디렉토리 설정
            output_dir = Path(base_dir) / "YOLODataset"
            output_dir.mkdir(exist_ok=True)
            
            # train/val 이미지, 라벨 디렉토리 생성
            for split in ['train', 'val']:
                (output_dir / 'images' / split).mkdir(parents=True, exist_ok=True)
                (output_dir / 'labels' / split).mkdir(parents=True, exist_ok=True)
            
            # 훈련 데이터 처리
            split_dir = Path(base_dir) / 'training'
            
            # 각 클래스 폴더 처리
            for class_folder in ['bear_export', 'boar_export', 'waterdeer_export']:
                class_path = split_dir / class_folder
                
                if not class_path.exists():
                    print(f"Warning: {class_path} does not exist")
                    continue
                    
                print(f"Processing {class_folder}...")
                
                # JSON 파일들 찾기
                json_files = list(class_path.glob('*.json'))
                
                # 무작위로 섞기
                random.shuffle(json_files)
                
                # train/val 분할
                num_train = int(len(json_files) * train_ratio)
                train_files = json_files[:num_train]
                val_files = json_files[num_train:]
                
                for split, files in zip(['train', 'val'], [train_files, val_files]):
                    print(f"Splitting {split} set ({len(files)} files)...")
                    
                    for json_file in files:
                        # JSON 파일 읽기
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # 이미지 파일 경로
                        image_name = data['imagePath']
                        image_path = class_path / image_name
                        
                        # 이미지 파일이 존재하는지 확인
                        if not image_path.exists():
                            print(f"Warning: Image file {image_path} not found")
                            continue
                        
                        # 이미지 크기
                        img_width = data['imageWidth']
                        img_height = data['imageHeight']
                        
                        # YOLO 라벨 파일 생성
                        label_name = Path(image_name).stem + '.txt'
                        label_path = output_dir / 'labels' / split / label_name
                        
                        # 이미지 복사
                        target_image_path = output_dir / 'images' / split / image_name
                        shutil.copy2(image_path, target_image_path)
                        
                        # 바운딩 박스들을 YOLO 형식으로 변환
                        yolo_annotations = []
                        
                        for shape in data['shapes']:
                            label = shape['label']
                            
                            # 클래스 ID 가져오기
                            if label not in class_mapping:
                                print(f"Warning: Unknown class '{label}' in {json_file}")
                                continue
                            
                            class_id = class_mapping[label]
                            
                            # rectangle 타입만 처리 (바운딩 박스)
                            if shape['shape_type'] == 'rectangle':
                                points = shape['points']
                                x1, y1 = points[0]
                                x2, y2 = points[1]
                                
                                # YOLO 형식으로 변환 (정규화된 중심점과 크기)
                                x_center = (x1 + x2) / 2.0 / img_width
                                y_center = (y1 + y2) / 2.0 / img_height
                                width = abs(x2 - x1) / img_width
                                height = abs(y2 - y1) / img_height
                                
                                yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
                        
                        # 라벨 파일 쓰기
                        with open(label_path, 'w') as f:
                            f.write('\n'.join(yolo_annotations))
            
            # dataset.yaml 파일 생성
            yaml_content = f"""path: {output_dir.absolute()}
        train: images/train
        val: images/val
        test: 
        
        names:
          0: bear
          1: boar
          2: waterdeer
        """
            
            yaml_path = output_dir / 'dataset.yaml'
            with open(yaml_path, 'w') as f:
                f.write(yaml_content)
            
            # 클래스 정보 파일 생성
            classes_path = output_dir / 'classes.txt'
            with open(classes_path, 'w') as f:
                f.write('bear\nboar\nwaterdeer')
            
            print(f"\n변환 완료!")
            print(f"출력 디렉토리: {output_dir}")
            print(f"dataset.yaml: {yaml_path}")
            print("\n클래스 매핑:")
            print("0: bear (thibetanus)")
            print("1: boar (scrofa)")
            print("2: waterdeer (inermis)")
        
        if __name__ == "__main__":
            # 기본 디렉토리 설정
            base_directory = r"C:\Users\AREU\Desktop\PolyProject\animal"
            
            # train/val 비율 설정 (예: 80% train, 20% val)
            train_ratio = 0.8
            
            # 변환 실행
            convert_labelme_to_yolo(base_directory, train_ratio)
        ```
        

✅ 처리부_객체 탐지

- YOLOv11 모델 학습. 커스텀 모델의 가중치를 불러옴.
    - 코드
        
        ```python
        from ultralytics.utils.callbacks.base import on_fit_epoch_end
        
        print("YOLOv11 모델을 로드합니다.")
        try:
            model = YOLO('best.pt') #클래스 추가하려면 여기 변경경
        except Exception as e:
            print(f"YOLOv11 모델 로드 중 오류 발생: {e}")
            print("인터넷 연결을 확인하거나, yolo11n.pt 파일이 제대로 다운로드되었는지 확인해주세요.")
            exit() # 오류 발생 시 스크립트 종료
        
        print("모델이 인식할 수 있는 기본 클래스 목록:")
        print(f"타입: {type(model.names)}, 개수: {len(model.names)}")
        print(model.names)
        print("-" * 30)
        
        # Early stopping 콜백 함수 정의
        def custom_on_fit_epoch_end(trainer):
            # 검증 데이터에 대한 결과 추출
            metrics = trainer.metrics
            
            # 현재 검증 지표 (mAP50-95)
            current_fitness = metrics.get('metrics/mAP50-95(B)', 0)
            
            # best_fitness 초기화 (처음 실행 시)
            if not hasattr(trainer, 'best_fitness'):
                trainer.best_fitness = 0
            
            # patience 초기화 (처음 실행 시)
            if not hasattr(trainer, 'patience_count'):
                trainer.patience_count = 0
            
            # 지표가 개선되었는지 확인
            if current_fitness > trainer.best_fitness:
                trainer.best_fitness = current_fitness  # best_fitness 업데이트
                trainer.patience_count = 0  # patience 카운터 리셋
                print(f'새로운 최고 성능 모델: mAP50-95 = {current_fitness:.4f}')
            else:
                trainer.patience_count += 1  # patience 카운터 증가
                print(f'성능 개선 없음: {trainer.patience_count}/{trainer.args.patience}')
                
                # patience 한계에 도달하면 훈련 중단
                if trainer.patience_count >= trainer.args.patience:
                    print(f'Early stopping 활성화: {trainer.patience_count} 에폭 동안 성능 개선 없음')
                    trainer.epoch = trainer.args.epochs + 1  # 훈련 종료 신호
                    
            return metrics
        
        # 콜백 함수 등록
        callbacks_list = model.callbacks.copy()  # 기존 콜백 복사
        callbacks_list["on_fit_epoch_end"] = [custom_on_fit_epoch_end]  # 사용자 정의 콜백 추가
        model.callbacks = callbacks_list  # 모델에 콜백 설정
        
        # 모델 훈련을 시작
        print("모델 훈련을 시작합니다.")
        results = model.train(
            data=CUSTOM_YAML_PATH, 
            epochs=25,  # 최대 에폭 수 (early stopping으로 더 일찍 종료될 수 있음)
            batch=4, 
            imgsz=640,
            patience=7,  # n에폭 동안 개선이 없으면 중단
            project=CUSTOM_RUNS_DIR,  # 커스텀 프로젝트 디렉토리
            name='train'  # 하위 폴더 이름 (예: custom_runs/train)
        )
        
        print("모델 훈련이 완료되었습니다.")
        # 훈련 결과는 지정된 디렉토리에 저장됩니다.
        print(f"훈련 결과는 '{os.path.join(CUSTOM_RUNS_DIR, 'train')}' 폴더에 저장됩니다.")
        print("-" * 30)
        ```
        

✅ 처리부_threading 라이브러리를 활용한 객체탐지, 영상업로드 동시 처리

- threading 라이브러리를 사용해 영상 압축 및 업로드와 관련된 처리를 백그라운드 스레드로 분리. 결과적으로 두 기능은 동시에 진행됨.
- 2초 이상 감지된 객체는 자동으로 영상 녹화 (커스텀 가능)
- 녹화된 영상 및 탐지 정보를 DB(Firebase Storage와 Firestore)에 자동 업로드
    - 코드 예제
        
        ```python
        import os
        import cv2
        import random
        import numpy as np
        import matplotlib.pyplot as plt
        from ultralytics import YOLO
        
        # 스크립트 파일이 포함된 폴더 경로를 지정합니다.
        PROJECT_DIR = r'C:\Users\AREU\Desktop\PolyProject'
        CUSTOM_RUNS_DIR = os.path.join(PROJECT_DIR, 'runs')  # 원하는 위치로 변경 가능
        
        # --- 설정 부분 ---
        # 데이터셋 기본 경로 설정
        DATASET_BASE_DIR = r'C:\Users\AREU\Desktop\PolyProject\animal\YOLODataset'
        
        # 1. 훈련된 모델 로드
        trained_model_path = os.path.join('runs', 'train', 'weights', 'best.pt')
        model = YOLO(trained_model_path)
        print(f"훈련된 모델을 로드했습니다: {trained_model_path}")
        
        import cv2
        from ultralytics import YOLO
        
        # 학습된 모델 경로
        MODEL_PATH = os.path.join(CUSTOM_RUNS_DIR, 'train', 'weights', 'best.pt')
        
        # 웹캠 활성화 (인덱스 0: 기본 웹캠)
        cap = cv2.VideoCapture(0)
        
        # 웹캠 해상도 설정 (옵션)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 너비
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 높이
        
        # 모델 로드
        model = YOLO(MODEL_PATH)
        
        # 데이터셋 구성 정보
        data_cf = {
            'train': os.path.join(DATASET_BASE_DIR, 'images', 'train').replace('\\', '/'),
            'val': os.path.join(DATASET_BASE_DIR, 'images', 'val').replace('\\', '/'),
            'nc': 3,  # 클래스 개수 (예: 'Cup' 하나면 1)
            'names': ['bear', 'boar', 'waterdeer']   # 명시된 클래스 이름 리스트
        }
        
        # 신뢰도 임계값 설정 
        CONFIDENCE_THRESHOLD = 0.75
        
        print("웹캠이 활성화되었습니다. 'q' 키를 눌러 종료하세요.")
        
        # 웹캠 프레임별 처리
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("웹캠에서 프레임을 읽을 수 없습니다.")
                break
        
            # 프레임에 대해 모델 추론
            results = model(frame)
        
            # 결과에서 bounding box 정보 추출 및 시각화
            for result in results:
                boxes = result.boxes  # 탐지된 객체의 bounding box 정보
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # bounding box 좌표
                    conf = box.conf.item()  # 신뢰도 (confidence)
                    cls = int(box.cls.item())  # 클래스 인덱스
                    label = f"{model.names[cls]} {conf:.2f}"  # 클래스 이름과 신뢰도
        
                    # 신뢰도 임계값 체크
                    if conf < CONFIDENCE_THRESHOLD:
                        continue  # 신뢰도가 낮으면 무시
        
                    # 명시된 클래스만 탐지 ('names'에 포함된 클래스만)
                    if model.names[cls] not in data_cf['names']:
                        continue  # 명시되지 않은 클래스는 무시
        
                    # bounding box 그리기
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # 라벨 텍스트 그리기
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
            # 결과 프레임 출력
            cv2.imshow('YOLO Webcam Detection', frame)
        
            # 'q' 키를 누르면 종료
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # 자원 해제
        cap.release()
        cv2.destroyAllWindows()
        
        print("웹캠 스트림이 종료되었습니다.")
        ```
        
    
    !image.png
    

✅ 구동부_로그인 관리

- FireStore Database와 연동하여 존재하는 ID인지 확인, 추후 탐지내역 조회에 사용
- 아이디 저장 기능을 제공으로 편의성 강화 (정상 : 메인화면 진입 / 비정상 : 안내팝업 출력)

!ID 저장 기능

ID 저장 기능

!ID 존재 여부 검사

ID 존재 여부 검사

✅ 구동부_탐지 내역 실시간 모니터링

- 고정형 CCTV 4대의 탐지내역이 존재하는 경우 탐지 당시의 영상(8~10초)가 출력
- 영상 하단에 각 CCTV별 탐지 정보 출력
- 기록이 없는 경우 빈 화면과 ‘기록 없음’ 표기
- 하단 Chart를 활용하여 객체별 당일 탐지 건수에 대한 통계자료 시각화.

!monitoring0704.gif

✅ 로그 기록 확인

- ID를 기준으로 전체 탐지 기록을 시간순으로 로그 형식 제공
(일자 / 시간 / 탐지동물 / 위치)
- 페이징 기능 탑재

!log.gif

✅ 객체 탐지 현황 분석을 위한 chart 제공

- 초기 값은 어플 실행 당일(1일) 로그데이터를 기준으로 chart 출력
- [라디오] 버튼을 이용해서 조회 기간 설정
- [직접선택] 시 [datepicker] 버튼을 활성화하고 사용자가 원하는 기간을 직접 지정 가능

!chart.gif

!chart1.gif

### 트러블 슈팅 (1/2)

🚨 문제 배경

DB 선택 과정에서 경량화되고 Mobile 환경에 최적화된 SQLite를 선택. 테이블을 구축하고 더미데이터를 넣어 정상적으로 DB가 구축 된 걸 확인하였으나 .db 파일의 저장 경로 확인 불가.
YOLO에서 탐지 기록을 저장하기 위해서는 .db 파일의 위치와 저장 방법을 고려해야 했고, 해당 파일을 다시 MAUI App에서 읽어와야 했고, 그에 따른 새로운 문제점이 지속적으로 발생함.
(로컬서버(FTP)구축, 저장방식, 실시간성 등)

💡 해결방법

추후 Jecson Nano등 H/W 환경이 구축되면 로컬서버가 필요하고, 메인PC 겸용으로 사용 가능.
그러나 현재 프로토타입은 H/W 구축이 불가하고, 실시간성을 위해 클라우드방식의 Firebase로 DB 변경.

1. SQLite 환경에서 data 업데이트 방식
    1. IDE에서 [adb prompt] 실행  - [.db] 파일을 내보내기 위한 명령어 실행
    
    !명령어 실행시 프로젝트 폴더에 새로운 data file이 복사되어 내보내진걸 확인 가능
    
    명령어 실행시 프로젝트 폴더에 새로운 data file이 복사되어 내보내진걸 확인 가능
    
    !SQLite 프로그램에서 .db 파일을 수기로 읽어와야하는 복잡한 방식.png)
    
    SQLite 프로그램에서 .db 파일을 수기로 읽어와야하는 복잡한 방식
    
2. DB 변경(SQLite → Firebase)

<aside>
💡

현재 .db파일은 adb prompt를 활용해서만 내보낼수 있음(코드 불가)

→ 수동으로 내보내고 불러와야 하는 단점이 있음.

해결방안
1. 로컬환경(FTP)을 구축해서 공유하는 방법
→ 로컬환경서버가 되는 PC가 꺼져있으면 저장이 안됨.
젯슨나노 등의 보드를 로컬환경으로 활용하고 계속 켜두는 방법이 좋음
2. 구글 드라이브등의 서버를 구축 → 유료 혹은 복잡함.
3. Firebase 클라우드 기반이며 정형,비정형 데이터 기 가능

</aside>

<aside>
💡

변경사유

1. SQLite는 가볍지만 2인 이상 작업의 경우 ’서버’가 필요함.
2. FireBase의 경우 클라우드

| 항목 | SQLite | FireBase |
| --- | --- | --- |
| 패키지 | sqlite-net-pcl | Google.Cloud.Firestore |
| 키여부 | 내장db | 비밀키필요 |
| 호환성 | 로컬서버로 내보내야 가능 | 실시간 클라우드 연동 가능 |
|  |  |  |
</aside>

### 트러블 슈팅 (2/2)

🚨 문제 배경

Chart를 사용하기 위한 패키지인 Microcharts.Maui와 SkiaSharp 패키지 설치 과정에서 버전충돌, 리소스를 못 찾는 문제점이 발생

💡 해결방법

Package 버전 설정 : MAUI net 8.0 환경과 호환되는 Package 버전 탐색

1. SkiaSharp [SKCanvasView] 사용시 Android 스타일 리소스가 추가되어야하며, 종종 누락되는 오류 발생 → 패키지 설치를 확인하거나 누락방지 설정을 수기로 추가해주어야함

```xml
<PropertyGroup>
  <AndroidUseLatestPlatformSdk>true</AndroidUseLatestPlatformSdk>
  <AndroidEnableSkiasharpSupport>true</AndroidEnableSkiasharpSupport> <!-- 이 줄 추가 -->
</PropertyGroup>

```

1. 오류 지속되어 SkiaSharp 관련 패키지 전체 삭제 후 최신 안정버전(3.119.0) 설치
2. MicroChart와 호환하려면 SkiaSharp(2.88.3)을 사용해야함. **(Chart 패키지끼리의 충돌)**
    
    !image.png
    

Resources는 자동으로 추가가 되는 요소이나, MAUI 불안정성으로 수기 기재가 필요.

1. SkiaSharp 관련 패키지 최신버전으로 업데이트
→ MicroChart와 호환성 문제 발생
2. NuGet 캐시 삭제
→ 리소스 충돌 원이이 될 수 있다고 해서 임시 캐시 삭제.
→ bin, obj 등 프로젝트 내 임시 캐시 폴더도 삭제 후 재시도
3. 잘못된 필드 토큰여부 확인
4. Platforms/Android/Resources/values/attrs.xml 파일에 접근하여 리소스 직접 추가

!https://github.com/dotnet/maui/issues/19645

https://github.com/dotnet/maui/issues/19645

# **프로젝트 성과**

- Labelme yolo, label me to yolo 등 데이터 가공 능력 습득
- Yolov11 커스텀 모델 제작 가능
- Yolo 비전 처리의 모든 구축 과정을 완료
- 실시간 객체 인식 시스템 기획 및 크로스플랫폼 앱(.NET MAUI)으로 구현
- YOLO 탐지 결과 시각화
- SQLite → Firebase 전환을 포함한 2종 DB 설계 및 실시간 동기화 시스템 구축
- 외부 패키지(Microcharts, SkiaSharp) 버전 충돌 해결을 통한 앱 안정성 확보
- 앱 전체 UI/UX 흐름 설계 및 기능 중심의 스토리보드·화면 목업 제작
