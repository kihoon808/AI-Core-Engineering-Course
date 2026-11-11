"""
실습 03: YOLO 포맷 라벨 파일 읽기
YOLO 라벨 파일(TXT)을 한 줄씩 읽어서 정규화된 좌표를 해석합니다.
각 줄은 '클래스 중심X 중심Y 너비 높이' 순서(0에서 1 사이 비율)입니다.
"""
from pathlib import Path
import os
import cv2

BASE = Path(__file__).resolve().parent
os.chdir(BASE)

names = ["square", "circle", "triangle"]
for image_path in sorted((BASE / "data/images/train").glob("*.png"))[:6]:
    # 이미지 파일명을 상대 경로로 읽습니다.
    image = cv2.imread(f"data/images/train/{image_path.name}")
    label_path = BASE / "data/labels/train" / (image_path.stem + ".txt")
    # >>> B04
    # 텍스트 파일을 읽고 줄 단위 리스트로 분리합니다.
    lines = label_path.read_text(encoding="utf-8").splitlines()
    # <<< B04
    print(image_path.name, "shape:", image.shape, "boxes:", len(lines))
    for line in lines:
        cls, cx, cy, width, height = map(float, line.split())
        print(" ", names[int(cls)], "normalized:", cx, cy, width, height)
