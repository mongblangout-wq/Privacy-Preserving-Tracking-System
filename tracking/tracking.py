import cv2
from ultralytics import YOLO

# 모델 로드 (yolov8n.pt 또는 yolov8s.pt)
model = YOLO('yolov8n.pt')

# 영상 경로 설정
video_path = 'data/MOT17-04_person_mosaic_strong.mp4'
cap = cv2.VideoCapture(video_path)

# 트래커 설정 ('bytetrack.yaml' 또는 'botsort.yaml')
tracker_type = 'bytetrack.yaml'

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output_tracked.mp4', fourcc, fps, (width, height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model.track(
        source=frame,
        persist=True,
        tracker=tracker_type,
        classes=[0],
        conf=0.3
    )

    annotated_frame = results[0].plot()

    cv2.imshow("Tracking Test", annotated_frame)
    out.write(annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()