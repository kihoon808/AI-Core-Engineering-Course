"""
기울어진 문서 이미지를 원근 변환(Perspective Transform)을 통해 반듯하게 보정합니다.
문서의 네 모서리 좌표를 직사각형 크기(1000x700)로 펴서 정면에서 본 형태로 변환합니다.
보정된 이미지에 적응형 이진화(Adaptive Threshold)를 적용하여 글자 가독성을 높입니다.
"""
from pathlib import Path
import os
import json
import re
import numpy as np
import pandas as pd
import cv2

base = Path(__file__).resolve().parent
# Windows 한글 경로 인식 오류를 방지하기 위해 작업 디렉토리를 변경합니다.
os.chdir(base)

data = base / 'data'
out = base / 'outputs'
out.mkdir(exist_ok=True)
lesson = json.loads((data / 'lesson.json').read_text(encoding='utf-8'))

# 상대 경로로 원근 왜곡된 이미지를 읽어옵니다.
image = cv2.imread('data/perspective.png')
corners = np.float32(lesson['perspective']['corners'])  # TL, TR, BR, BL 제공
size = (1000, 700)  # width, height
# 원본 사각형 모서리를 목표 직사각형 좌표로 매핑하는 변환 행렬을 계산합니다.
matrix = cv2.getPerspectiveTransform(corners, np.float32([[0,0],[999,0],[999,699],[0,699]]))
# TODO A01
# 투시 변환 행렬을 적용하여 이미지를 반듯한 직사각형 형태로 보정(펴기)합니다.
rectified = cv2.warpPerspective(image, matrix, size)
# TODO 끝 A01
gray = cv2.cvtColor(rectified, cv2.COLOR_BGR2GRAY)
# 조명 변화에 강한 가우시안 적응형 이진화를 수행합니다.
adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11)
cv2.imwrite('outputs/p01_rectified.png', rectified)
cv2.imwrite('outputs/p01_adaptive.png', adaptive)
print('before:', image.shape, 'after:', rectified.shape)
print('알려진 모서리로 보정했습니다. 모서리 자동 검출이 아닙니다.')
