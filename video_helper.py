import cv2
import os
import shutil
import sys
from pathlib import Path

def extract_frames(video_path, output_dir):
    print(f"[*] Extracting frames from {video_path} to {output_dir}...")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"[!] Error: Could not open video {video_path}")
        sys.exit(1)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_name = f"frame_{frame_count:04d}.jpg"
        cv2.imwrite(os.path.join(output_dir, frame_name), frame)
        frame_count += 1

    cap.release()
    print(f"[*] Successfully extracted {frame_count} frames.")

def merge_frames(frames_dir, output_video_path, fps=30):
    print(f"[*] Merging frames from {frames_dir} into {output_video_path}...")
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])
    
    if not frame_files:
        print(f"[!] Error: No frames found in {frames_dir}")
        sys.exit(1)

    # Read first frame to get size
    first_frame = cv2.imread(os.path.join(frames_dir, frame_files[0]))
    height, width, _ = first_frame.shape

    os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    if not writer.isOpened():
        print(f"[!] Error: Could not initialize VideoWriter for {output_video_path}")
        sys.exit(1)

    for i, file_name in enumerate(frame_files):
        frame = cv2.imread(os.path.join(frames_dir, file_name))
        writer.write(frame)
        if (i + 1) % 50 == 0 or (i + 1) == len(frame_files):
            print(f"[*] Merged {i + 1}/{len(frame_files)} frames...")

    writer.release()
    print(f"[*] Successfully created output video at {output_video_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python video_helper.py extract <video_path> <output_dir>")
        print("  python video_helper.py merge <frames_dir> <output_video_path> <fps>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "extract":
        extract_frames(sys.argv[2], sys.argv[3])
    elif cmd == "merge":
        fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        merge_frames(sys.argv[2], sys.argv[3], fps)
    else:
        print(f"[!] Unknown command: {cmd}")
        sys.exit(1)
