# download_face_model.py
"""
yolov8n-face.pt는 ultralytics 공식 배포 모델이 아니라서 YOLO("yolov8n-face.pt")로
자동 다운로드되지 않습니다. 아래 스크립트로 사전에 받아두세요.

사용법:
    python download_face_model.py
"""
import requests
from pathlib import Path
from config import FACE_MODEL_PATH

# lindevs/yolov8-face 릴리즈 (ultralytics YOLO()로 바로 로드 가능한 체크포인트)
FACE_MODEL_URL = "https://github.com/lindevs/yolov8-face/releases/latest/download/yolov8n-face-lindevs.pt"


def main():
    if FACE_MODEL_PATH.exists():
        print(f"[INFO] 이미 존재합니다: {FACE_MODEL_PATH}")
        return

    print(f"[INFO] 다운로드 중: {FACE_MODEL_URL}")
    resp = requests.get(FACE_MODEL_URL, stream=True, timeout=60)
    resp.raise_for_status()
    with open(FACE_MODEL_PATH, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"[SUCCESS] 저장 완료: {FACE_MODEL_PATH}")


if __name__ == "__main__":
    main()
