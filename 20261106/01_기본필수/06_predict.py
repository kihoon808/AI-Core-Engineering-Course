"""
실습 06: YOLO 추론 파이프라인
검증용 이미지 폴더(val)를 읽어서 객체 탐지(Predict)를 실행합니다.
검출된 박스 좌표, 클래스 ID, 확신도를 추출하여 CSV로 저장합니다.
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

# data/demo.pt 가중치를 로드합니다.
model = YOLO(str(BASE / "data/demo.pt"))
rows = []; counts = []

# >>> B07
# 검증 이미지에 대해 conf=0.25, imgsz=160, CPU 옵션으로 추론을 수행합니다.
results = model.predict(source="data/images/val", conf=0.25, imgsz=160, device="cpu", verbose=False)
# <<< B07

for result in results:
    name = Path(result.path).stem
    counts.append({"image": name, "detections": len(result.boxes)})
    # 한글 경로 호환을 위해 상대 경로로 저장합니다.
    cv2.imwrite("p06_" + name + ".png", result.plot())
    for box, cls, score in zip(result.boxes.xyxy.cpu().tolist(), result.boxes.cls.cpu().tolist(), result.boxes.conf.cpu().tolist()):
        rows.append([name, int(cls), score, *box])

pd.DataFrame(rows, columns=["image", "class_id", "confidence", "x1", "y1", "x2", "y2"]).to_csv("p06_predictions.csv", index=False)
pd.DataFrame(counts).to_csv("p06_counts.csv", index=False)
print("처리 이미지:", len(counts), "탐지 수:", len(rows))
