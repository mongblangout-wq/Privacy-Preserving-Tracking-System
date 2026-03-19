# config.py
import os
from pathlib import Path

# --- 프로젝트 경로 설정 ---
PROJECT_DIR = Path(os.getcwd())
# 필요시 실제 데이터 경로로 수정하세요 (예: Path("/content/drive/..."))
MOT17_ROOT = PROJECT_DIR / 'MOT17_Full' / 'MOT17' / 'train'
MOT20_ROOT = PROJECT_DIR / 'MOT20_Full' / 'MOT20' / 'train'
SAVE_ROOT = PROJECT_DIR / 'Final_Results'

# --- [중요] 사용자 정의 비식별화 파라미터 ---
# L = min(width, height) 기준 비율
PARAMS = {
    "FACE_BLUR":    {"weak": 0.2,  "medium": 0.4,  "strong": 0.6},   # 약 0.2L, 0.4L, 0.6L
    "FACE_MOSAIC":  {"weak": 0.1,  "medium": 0.2,  "strong": 0.3},   # 약 0.1L, 0.2L, 0.3L
    "PERSON_BLUR":  {"weak": 0.15, "medium": 0.3,  "strong": 0.5},   # 약 0.15L, 0.3L, 0.5L
    "PERSON_MOSAIC":{"weak": 0.03, "medium": 0.06, "strong": 0.09}  # 약 0.03L, 0.06L, 0.09L
}

# --- 시퀀스별 프레임 구간 설정 ---
SEQ_CONFIG = {
    'MOT17-04': {'start': 300, 'end': 900},
    'MOT17-05': {'start': 1,   'end': 601},
    'MOT17-09': {'start': 1,   'end': 526},
    'MOT17-11': {'start': 300, 'end': 900},
    'MOT17-13': {'start': 1,   'end': 601},
    'MOT20-02': {'start': 200, 'end': 800},
}

LEVELS = ['weak', 'medium', 'strong']