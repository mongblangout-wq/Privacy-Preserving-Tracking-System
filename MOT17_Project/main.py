#main.py
import cv2
from ultralytics import YOLO
from config import PARAMS, SEQ_CONFIG, MOT17_ROOT, MOT20_ROOT, SAVE_ROOT, LEVELS
from deid_utils import apply_anonymization


class AnonymizationManager:
    def __init__(self, sequence_name):
        self.seq_name = sequence_name
        self.config = SEQ_CONFIG[sequence_name]

        # 경로 결정 (MOT17 vs MOT20)
        root = MOT20_ROOT if "MOT20" in sequence_name else MOT17_ROOT
        suffix = "" if "MOT20" in sequence_name else "-SDP"
        self.source_path = root / f"{sequence_name}{suffix}" / 'img1'

        self.save_dir = SAVE_ROOT / sequence_name
        self.save_dir.mkdir(parents=True, exist_ok=True)

        # 모델 로드
        print(f"📦 모델 로드 중... ({sequence_name})")
        self.person_model = YOLO("yolov8n.pt")
        self.face_model = YOLO("yolov8n-face.pt")

    def run(self):
        frame_files = sorted(list(self.source_path.glob("*.jpg")))
        target_frames = frame_files[self.config['start'] - 1: self.config['end']]

        if not target_frames:
            print(f"❌ 프레임을 찾을 수 없습니다: {self.source_path}")
            return

        writers = {}
        print(f"🚀 처리 시작: {len(target_frames)} 프레임 대상")

        try:
            for i, frame_path in enumerate(target_frames):
                frame = cv2.imread(str(frame_path))
                if frame is None: continue

                # 검출 (프레임당 1회 수행)
                p_res = self.person_model(frame, verbose=False, conf=0.3, classes=[0])[0]
                p_boxes = p_res.boxes.xyxy.cpu().numpy() if p_res.boxes is not None else []

                f_res = self.face_model(frame, verbose=False, conf=0.3)[0]
                f_boxes = f_res.boxes.xyxy.cpu().numpy() if f_res.boxes is not None else []

                # --- 12가지 조합 비식별화 처리 ---
                for lv in LEVELS:
                    # 얼굴 (Face)
                    self._save(frame, f_boxes, "blur", PARAMS["FACE_BLUR"][lv], f"face_blur_{lv}", writers)
                    self._save(frame, f_boxes, "mosaic", PARAMS["FACE_MOSAIC"][lv], f"face_mosaic_{lv}", writers)
                    # 사람 (Person)
                    self._save(frame, p_boxes, "blur", PARAMS["PERSON_BLUR"][lv], f"person_blur_{lv}", writers)
                    self._save(frame, p_boxes, "mosaic", PARAMS["PERSON_MOSAIC"][lv], f"person_mosaic_{lv}", writers)

                if i % 50 == 0:
                    print(f"  > Progress: {i}/{len(target_frames)}...")

        finally:
            for w in writers.values(): w.release()
            print(f"✅ 완료! 저장 위치: {self.save_dir}")

    def _save(self, frame, boxes, method, ratio, name, writers):
        """비식별화 적용 후 영상 저장"""
        out = apply_anonymization(frame, boxes, method, ratio)

        if name not in writers:
            h, w = frame.shape[:2]
            path = str(self.save_dir / f"{name}.avi")
            writers[name] = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'XVID'), 30.0, (w, h))

        writers[name].write(out)


if __name__ == "__main__":
    # 실행하고 싶은 시퀀스 리스트
    targets = [
        "MOT17-04",
        "MOT17-05",
        "MOT17-09",
        "MOT17-11",
        "MOT17-13",
        "MOT20-02"]
    for target in targets:
        manager = AnonymizationManager(target)
        manager.run()