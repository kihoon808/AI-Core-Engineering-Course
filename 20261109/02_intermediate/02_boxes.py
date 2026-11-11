"""
OCR 엔진이 감지한 개별 단어의 바운딩 박스(Bounding Box) 좌표를 원본 이미지 위에 시각화합니다.
각 단어 위치를 파란색 직사각형 박스로 표시하여 인식 영역을 점검합니다.
Tesseract의 다양한 페이지 분할 모드(PSM: Page Segmentation Mode)별 텍스트 추출 결과를 비교합니다.
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

doc = lesson['documents']['doc01']
image = cv2.imread(f"data/{doc['file']}")
for word in doc['ocr']['tokens']:
    x1, y1, x2, y2 = word['bbox']
# TODO A02
    # 각 단어의 바운딩 박스 좌표에 파란색(BGR: 255, 0, 0) 사각형을 그립니다.
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 1)
# TODO 끝 A02
cv2.imwrite('outputs/p02_word_boxes.png', image)
# PSM을 실시간으로 반복 호출하지 않고 모드와 적합한 입력을 설계합니다.
print('단어:', len(doc['ocr']['tokens']), 'backend:', doc['ocr']['backend'])
print('PSM 3: 전체 문서 / PSM 6: 균일한 글 블록 / PSM 7: 한 줄 crop')
for record in lesson['psm_records']:
    print('PSM', record['psm'], record['region'], '->', repr(record['text'][:65]))
print('PSM 7은 한 줄 crop입니다. 전체 페이지와 입력 범위가 다르므로 CER을 직접 순위화하지 않습니다.')
