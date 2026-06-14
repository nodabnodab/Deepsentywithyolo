import os
import json
import shutil
from pathlib import Path

def convert_labelme_to_yolo(base_dir):
    """
    LabelMe JSON 파일들을 YOLO 형식으로 변환. 두번째로 할 일임. 
    이미 분할된 train/val 구조를 유지하면서 클래스를 통합
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
    
    # 훈련/검증 데이터 처리
    for split in ['training', 'validation']:
        yolo_split = 'train' if split == 'training' else 'val'
        split_dir = Path(base_dir) / split
        
        # 각 클래스 폴더 처리
        for class_folder in ['bear_export', 'boar_export', 'waterdeer_export']:
            class_path = split_dir / class_folder
            
            if not class_path.exists():
                print(f"Warning: {class_path} does not exist")
                continue
                
            print(f"Processing {split}/{class_folder}...")
            
            # JSON 파일들 찾기
            json_files = list(class_path.glob('*.json'))
            
            for json_file in json_files:
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
                label_path = output_dir / 'labels' / yolo_split / label_name
                
                # 이미지 복사
                target_image_path = output_dir / 'images' / yolo_split / image_name
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
    
    # 변환 실행
    convert_labelme_to_yolo(base_directory)
