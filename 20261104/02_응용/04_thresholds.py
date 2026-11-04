from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

import csv
import json
from time import perf_counter
Path("outputs").mkdir(exist_ok=True)

gray = cv2.imread("data/scene.png", cv2.IMREAD_GRAYSCALE)
fixed_t, fixed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
# Otsu로 임계값을 자동 결정하세요. 반환값 두 개를 otsu_t와 otsu로 받습니다.
#이미지의 흑백 히스토그램을 분석하여, 배경 클래스와 전경 클래스 사이의 클래스 간 분산(Between-class Variance)을 수학적으로 최대화하는 최적의 분기점(T)을 자동으로 찾아내 otsu_t로 반환합니다.
otsu_t, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
rows = []
for name, threshold, binary in [("fixed", fixed_t, fixed), ("otsu", otsu_t, otsu)]:
    result = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel) #팽창(Dilation) 후 침식(Erosion) 연산입니다.
    cv2.imwrite(f"outputs/p04_{name}_binary.png", binary)
    cv2.imwrite(f"outputs/p04_{name}_close.png", result)
    rows.append([name, threshold, int(np.count_nonzero(binary)), int(np.count_nonzero(result))])

with open("outputs/p04_foreground.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["method", "threshold", "before", "after"]); w.writerows(rows)
print(rows)
