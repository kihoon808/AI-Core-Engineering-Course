"""
실습 01: 정답 박스(Ground Truth) 시각화
정답 좌표(x1, y1, x2, y2)를 읽어서 원본 이미지 위에 사각형 박스를 그립니다.
정답 데이터에는 확신도(confidence)가 없음을 확인합니다.
"""
from pathlib import Path
import os
import cv2
import pandas as pd

BASE = Path(__file__).resolve().parent
# 한글 경로 인코딩 문제를 방지하기 위해 작업 디렉토리를 현재 파일 위치로 맞춥니다.
os.chdir(BASE)

image = cv2.imread("data/scene.png")
boxes = pd.read_csv("data/boxes_gt.csv")
result = image.copy()  # 그릴 배열을 복사하여 원본을 보존합니다.

for row in boxes.itertuples():
    # >>> B01
    # BGR 초록색으로 사각형 박스를 그립니다.
    cv2.rectangle(result, (int(row.x1), int(row.y1)), (int(row.x2), int(row.y2)), (0, 255, 0), thickness=2)
    # <<< B01
    print("class:", row.class_id, "xyxy:", row.x1, row.y1, row.x2, row.y2, "GT confidence: N/A")

cv2.imwrite("p01_boxes.png", result)
print("shape:", image.shape, "저장: p01_boxes.png")
