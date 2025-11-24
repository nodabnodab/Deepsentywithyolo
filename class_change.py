import os
from pathlib import Path

def update_label_class_id(label_dir, old_class_id, new_class_id):
    """
    지정된 디렉토리의 모든 .txt 라벨 파일에서 특정 클래스 ID를 새로운 ID로 변경합니다.
    """
    label_path = Path(label_dir)
    if not label_path.is_dir():
        print(f"Error: Directory not found - {label_dir}")
        return

    print(f"Processing .txt files in: {label_dir}")
    updated_files_count = 0
    for txt_file in label_path.glob("*.txt"):
        print(f"  Processing file: {txt_file.name}")
        lines_changed_in_file = False
        new_content = []
        try:
            with open(txt_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if parts and parts[0] == str(old_class_id):
                        parts[0] = str(new_class_id)
                        new_content.append(" ".join(parts))
                        lines_changed_in_file = True
                    else:
                        new_content.append(line.strip()) # 원본 라인 유지 (공백 제거)

            if lines_changed_in_file:
                with open(txt_file, 'w') as f:
                    f.write("\n".join(new_content))
                    # YOLO 라벨 파일은 마지막에 개행 문자가 있는 경우가 많으므로,
                    # 내용이 있다면 개행 추가 (필요에 따라 조절)
                    if new_content:
                        f.write("\n")
                updated_files_count += 1
                print(f"    Updated class ID in {txt_file.name}")
            else:
                print(f"    No lines with class ID '{old_class_id}' found in {txt_file.name}")

        except Exception as e:
            print(f"    Error processing file {txt_file.name}: {e}")

    print(f"\nFinished processing. Total files updated: {updated_files_count}")

if __name__ == "__main__":
    # 여기에 human 라벨 파일들이 있는 실제 경로를 입력하세요.
    # 예시: human_label_directory = r"C:\Users\AREU\Desktop\PolyProject\new_human_data\labels"
    human_label_directory = r"C:\Users\AREU\Desktop\PolyProject\animal\check\labels\val" # <<--- 이 경로를 수정하세요!

    old_id = 0  # 변경 전 클래스 ID
    new_id = 3  # 변경 후 클래스 ID (human)

    if human_label_directory == r"C:\Users\AREU\Desktop\PolyProject\animal\check\labels\val\export":
        print("Please update 'human_label_directory' with the actual path to your new human label files.")
    else:
        update_label_class_id(human_label_directory, old_id, new_id)