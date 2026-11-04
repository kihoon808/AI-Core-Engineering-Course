from pathlib import Path
import os
import cv2
import numpy as np

# 제공 코드: 어느 작업 폴더에서 실행해도 현재 파일 옆의 입력을 읽습니다.
# OpenCV에는 영문 상대 경로를 전달합니다. 원본 파일은 덮어쓰지 않습니다.
os.chdir(Path(__file__).resolve().parent)

image = cv2.imread("scene.png")
# image를 Gray와 RGB로 각각 변환하여 gray, rgb에 넣으세요. 두 번째 인자는 변환 코드입니다.

#3개 채널의 가중 평균(Y = 0.299 * R + 0.587 * G + 0.114 * B)을 계산하여 (H, W) 형태의 2차원 단일 채널 행렬로 압축합니다.
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#메모리의 0번 채널(Blue)과 2번 채널(Red)의 위치를 교환합니다.   
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#이미지를 224x224 해상도(딥러닝 백본 모델의 표준 입력 크기)로 리사이징합니다.
small = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

cv2.imwrite("p02_gray.png", gray)
cv2.imwrite("p02_small.png", small)
# RGB 배열은 화면 표시용입니다. imwrite에 그대로 넣지 않습니다.

print("Gray shape:", gray.shape) # 출력: (H, W) 형태의 2차원
print("RGB 빨강:", rgb[30, 30].tolist()) # 출력: [R, G, B] 순서로 적재
print("Resize shape:", small.shape)

"""
cv2.imwrite()는 기본적으로 입력 3채널 배열을 BGR 순서로 취급하여 인코딩합니다.
만약 RGB로 변환된 rgb 배열을 cv2.imwrite()에 그대로 전달하면,
Red와 Blue 채널이 다시 반전되어 푸르스름하게 왜곡된(Smurf 효과) 결과물이 저장됩니다.
반대로 Matplotlib(plt.imshow())이나 웹 브라우저 UI는 RGB 순서를 요구하므로,
표시용(Visualization) 라이브러리와 입출력(I/O) 엔진의 채널 순서 차이를 반드시 분리해서 관리해야 합니다.
"""
