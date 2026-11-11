"""
실습 01: 바운딩 박스 좌표계 변환 (xyxy -> 정규화 cxcywh)
절대 픽셀 좌표(x1, y1, x2, y2)를 YOLO 표준인 정규화 중심점과 크기(0~1)로 변환합니다.
역변환을 거쳐 원래 좌표로 복원했을 때 오차가 0인지 확인합니다.
"""
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
out = BASE / "outputs"; out.mkdir(exist_ok=True)
table = pd.read_csv(BASE / "data/boxes_gt.csv")
b = table[["x1", "y1", "x2", "y2"]].to_numpy(float); width, height = 160, 128

# >>> A01
# 중심 좌표와 너비/높이를 계산하고 각 축의 크기로 나누어 정규화합니다.
cx = (b[:, 0] + b[:, 2]) / 2.0 / width
cy = (b[:, 1] + b[:, 3]) / 2.0 / height
w = (b[:, 2] - b[:, 0]) / width
h = (b[:, 3] - b[:, 1]) / height
yolo = np.column_stack((cx, cy, w, h))
# <<< A01

pixel = yolo * np.array([width, height, width, height])
restored = np.column_stack((pixel[:, 0] - pixel[:, 2] / 2, pixel[:, 1] - pixel[:, 3] / 2, pixel[:, 0] + pixel[:, 2] / 2, pixel[:, 1] + pixel[:, 3] / 2))
print("최대 왕복 오차(px):", float(np.max(np.abs(b - restored))))
pd.DataFrame(yolo, columns=["cx", "cy", "w", "h"]).to_csv(out / "yolo_coordinates.csv", index=False)
