"""
실습 01: 문서 이미지 그레이스케일 변환 및 Otsu 이진화
BGR 컬러 이미지를 1채널 Gray로 변환한 뒤, Otsu 알고리즘을 사용해 최적 임계값으로 흑백 이진화합니다.
원본 이미지는 보존하며 p01_* 파일로 결과를 저장합니다.
"""
from pathlib import Path
import os
import cv2

base = Path(__file__).resolve().parent
os.chdir(base)

for name in ['doc01', 'doc02', 'doc03']:
    image = cv2.imread(f'{name}.png')
    # 아래 두 줄만 완성합니다. 출력은 채널이 없는 (높이, 너비) 배열입니다.
# TODO B01
    # BGR 이미지를 그레이스케일로 변환하고 Otsu 알고리즘으로 자동 이진화합니다.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# TODO 끝 B01
    cv2.imwrite(f'p01_{name}_gray.png', gray)
    cv2.imwrite(f'p01_{name}_binary.png', binary)
    print(name, 'shape:', gray.shape, 'threshold:', threshold)
