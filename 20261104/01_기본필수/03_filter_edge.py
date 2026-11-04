from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

image = cv2.imread("noisy.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #1채널 흑백 이미지로 변환

#가우시안 블러 적용: 커널 크기 (5, 5), 표준편차 sigmaX = 0 (자동 계산)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

#캐니 엣지 검출 적용: 하한 임곗값 80, 상한 임곗값 160
edge = cv2.Canny(blur, 80, 160)

cv2.imwrite("p03_blur.png", blur)
cv2.imwrite("p03_edge.png", edge)
print("설정: Gaussian (5,5), sigmaX=0, Canny 80/160")
print("Shape:", blur.shape, edge.shape)
print("Edge 픽셀:", int(np.count_nonzero(edge)))
