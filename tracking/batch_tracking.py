import sys
from pathlib import Path
from ultralytics import YOLO

models = ['yolov8n.pt', 'yolov8s.pt']
trackers = ['bytetrack.yaml', 'botsort.yaml']

video_dir = Path("Final_Results")
if not video_dir.exists():
    video_dir = Path("../Final_Results")

video_files = list(video_dir.rglob("*.avi")) + list(video_dir.rglob("*.mp4"))

if not video_files:
    print(f"[ERROR] '{video_dir}' 폴더 내에 영상이 존재하지 않습니다.")
    print("먼저 anonymization/run_anonymize.py를 실행하여 영상을 생성했는지 확인하세요.")
    sys.exit(1)

print(f"[INFO] 총 {len(video_files)}개의 비식별화 영상 감지 완료. 트래킹을 시작합니다.")

for model_name in models:
    model = YOLO(model_name)
    
    for tracker in trackers:
        tracker_name = tracker.split('.')[0]
        
        for video_path in video_files:
            print(f"[RUNNING] Model: {model_name} | Tracker: {tracker_name} | Video: {video_path.name}")
            
            model.track(
                source=str(video_path),
                tracker=tracker,
                persist=True,
                classes=[0],
                conf=0.3,
                save=True,       
                save_txt=True,  
                project='runs/track_results',
                name=f"{video_path.stem}_{model_name.replace('.pt', '')}_{tracker_name}",
                exist_ok=True,
                verbose=False
            )

print("[DONE] 모든 비식별화 영상 트래킹 완료!")