from pathlib import Path
from ultralytics import YOLO

models = ['yolov8n.pt', 'yolov8s.pt']
trackers = ['bytetrack.yaml', 'botsort.yaml']
video_dir = Path('data/anonymized_videos') 
video_files = list(video_dir.glob("*.avi")) + list(video_dir.glob("*.mp4"))

for model_name in models:
    model = YOLO(model_name)
    
    for tracker in trackers:
        tracker_name = tracker.split('.')[0]
        
        for video_path in video_list:
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