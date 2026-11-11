"""
실습 07~08: YOLO 영상 객체 탐지 및 실시간 다중 객체 추적(Tracking)
단일 이미지 추론 결과와 비디오(AVI) 스트림 추적 결과를 통합합니다.
ByteTrack 알고리즘을 사용해 프레임 간 동일 객체에 일관된 ID를 부여합니다.
"""
from pathlib import Path
import os
import cv2
import torch
import pandas as pd
from ultralytics import YOLO

BASE = Path(__file__).resolve().parent
os.chdir(BASE)
torch.set_num_threads(1)

model = YOLO(str(BASE / "data/demo.pt"))
rows = []
for r in model.predict(source="data/images/val", conf=0.25, imgsz=160, device="cpu", verbose=False):
    for box, cls, score in zip(r.boxes.xyxy.cpu().tolist(), r.boxes.cls.cpu().tolist(), r.boxes.conf.cpu().tolist()):
        rows.append([Path(r.path).name, int(cls), score, *box])
pd.DataFrame(rows, columns=["image", "class_id", "confidence", "x1", "y1", "x2", "y2"]).to_csv("p07_predictions.csv", index=False)

# 새 영상은 새 모델 인스턴스로 시작하여 이전 추적 상태를 이어붙이지 않습니다.
tracker = YOLO(str(BASE / "data/demo.pt"))
cap = cv2.VideoCapture("data/demo.avi")
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
cap.release()

writer = cv2.VideoWriter("p07_tracked.avi", cv2.VideoWriter_fourcc(*"MJPG"), fps, size)
tracks = []; frame_rows = []

# >>> B08
# 비디오 스트림에 대해 ByteTrack 기반 추적 제너레이터를 생성합니다.
results = tracker.track(source="data/demo.avi", stream=True, persist=False, verbose=False)
# <<< B08

for frame, result in enumerate(results):
    writer.write(result.plot())
    frame_rows.append([frame, len(result.boxes)])
    if result.boxes.id is not None:
        for box, cls, score, tid in zip(result.boxes.xyxy.cpu().tolist(), result.boxes.cls.cpu().tolist(), result.boxes.conf.cpu().tolist(), result.boxes.id.cpu().tolist()):
            tracks.append([frame, int(tid), int(cls), score, *box])
writer.release()

# >>> B09
# 추적 결과(프레임, 트랙ID, 클래스, 확신도, 좌표)를 CSV 파일로 저장합니다.
pd.DataFrame(tracks, columns=["frame", "track_id", "class_id", "confidence", "x1", "y1", "x2", "y2"]).to_csv("p07_tracks.csv", index=False)
# <<< B09

pd.DataFrame(frame_rows, columns=["frame", "detections"]).to_csv("p07_frames.csv", index=False)
print("입력 fps/size:", fps, size, "처리 Frame:", len(frame_rows))
print("실습 08: 설정을 바꾸지 말고 다시 실행해 Frame 수·CSV·영상을 확인하세요.")
