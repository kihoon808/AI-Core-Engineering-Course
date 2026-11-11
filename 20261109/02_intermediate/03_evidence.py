"""
라벨(DATE, SUPPLIER, TOTAL)의 공간적 위치를 기준으로 실제 값에 해당하는 단어를 추출합니다.
동일한 블록, 문단, 줄에 있으면서 라벨 오른쪽(x축 기준)에 위치한 단어들을 하나의 필드로 묶습니다.
추출된 필드의 값, 인식 신뢰도, 원본 이미지 좌표(bbox)를 함께 저장하여 추적 가능성을 확보합니다.
"""
from pathlib import Path
import json
import re
import numpy as np
import pandas as pd
import cv2
base = Path(__file__).resolve().parent
data = base / 'data'
out = base / 'outputs'
out.mkdir(exist_ok=True)
lesson = json.loads((data / 'lesson.json').read_text(encoding='utf-8'))

doc = lesson['documents']['doc01']
words = doc['ocr']['tokens']
fields = {}
for key, label in [('issued_at','DATE:'), ('supplier','SUPPLIER:'), ('total_amount','TOTAL:')]:
    anchor = next(w for w in words if w['text'] == label)
    # 같은 block/paragraph/line이고 라벨 오른쪽에 있는 단어만 선택합니다.
# TODO A03
    # 기준 라벨과 같은 줄(block, paragraph, line)에 속하고 라벨 오른쪽(x좌표 이상)에 있는 단어들을 필터링합니다.
    selected = [w for w in words if w['block'] == anchor['block'] and w['paragraph'] == anchor['paragraph'] and w['line'] == anchor['line'] and w['bbox'][0] >= anchor['bbox'][2]]
# TODO 끝 A03
    raw = ' '.join(w['text'] for w in selected)
    value = int(raw) if key == 'total_amount' else raw
    box = [min(w['bbox'][0] for w in selected),min(w['bbox'][1] for w in selected),max(w['bbox'][2] for w in selected),max(w['bbox'][3] for w in selected)]
    fields[key] = {'raw': raw, 'value': value, 'confidence': min(w['conf'] for w in selected), 'bbox': box, 'coordinate_space':'original_pixels'}
(out / 'p03_evidence.json').write_text(json.dumps(fields, ensure_ascii=False, indent=2), encoding='utf-8')
print({k:v['value'] for k,v in fields.items()})
