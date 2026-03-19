#deid_utils.py

import cv2
import numpy as np


def clamp_box(x1, y1, x2, y2, W, H):
    """이미지 범위를 벗어나지 않도록 좌표 조정"""
    x1, x2 = max(0, min(W - 1, int(x1))), max(0, min(W, int(x2)))
    y1, y2 = max(0, min(H - 1, int(y1))), max(0, min(H, int(y2)))
    return (x1, y1, x2, y2) if x2 > x1 and y2 > y1 else None


def safe_gaussian_blur(roi, L, ratio):
    """L 기준 가우시안 블러 (커널 사이즈 홀수 보장)"""
    h, w = roi.shape[:2]
    k = max(1, int(L * ratio))
    if k % 2 == 0: k += 1

    # ROI 크기보다 커널이 커지지 않도록 제한
    max_k = max(1, min(h, w) // 2 * 2 - 1)
    k = min(k, max_k) if k > 1 else 1
    if k % 2 == 0: k = max(1, k - 1)

    return cv2.GaussianBlur(roi, (k, k), 0)


def mosaic_roi(roi, L, ratio):
    """L 기준 모자이크 효과"""
    b = max(1, int(L * ratio))
    h, w = roi.shape[:2]
    tw, th = max(1, w // b), max(1, h // b)

    tmp = cv2.resize(roi, (tw, th), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(tmp, (w, h), interpolation=cv2.INTER_NEAREST)


def apply_anonymization(frame_bgr, boxes_xyxy, method, ratio):
    """박스 리스트에 대해 비식별화 적용"""
    out = frame_bgr.copy()
    H, W = out.shape[:2]

    for box in boxes_xyxy:
        bb = clamp_box(box[0], box[1], box[2], box[3], W, H)
        if bb is None: continue

        x1, y1, x2, y2 = bb
        roi = out[y1:y2, x1:x2]
        if roi.size == 0: continue

        L = min(x2 - x1, y2 - y1)  # 짧은 변 기준
        if method == "blur":
            out[y1:y2, x1:x2] = safe_gaussian_blur(roi, L, ratio)
        else:
            out[y1:y2, x1:x2] = mosaic_roi(roi, L, ratio)
    return out