"""
추출 값의 정답 일치 여부와 원문 내 근거 존재 여부를 분리하여 평가합니다.
단순히 값만 맞힌 경우와 실제 문서 내 근거까지 온전하게 존재하는 경우를 세분화하여 분석합니다.
정답 라벨 데이터는 성능 평가 단계에서만 비교 검증 용도로 엄격히 제한하여 사용합니다.
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

rows = []
for name, doc in lesson['documents'].items():
    for item in doc['mock_vlm']['responses']:
         # ========================================================
        # TODO A05: Mock VLM 답변과 실제 정답 비교
        # ========================================================
        # VLM 답변값(answer)과 정답 데이터(truth)의 해당 필드 값을 정확히 일치하는지 비교합니다.
        exact = bool(item['answer'] == doc['truth'][item['field']])
        # TODO 끝 A05
        grounded = item['evidence'] in doc['ocr']['text']
        rows.append({'document_id':name, 'field':item['field'], 'backend':'mock', 'exact':exact, 'evidence_found':grounded, 'review':not grounded})
table = pd.DataFrame(rows)
table.to_csv(out / 'p05_scores.csv', index=False, encoding='utf-8-sig')
print('값 일치:', int(table['exact'].sum()), '/', len(table))
print('값과 문자열 근거:', int((table['exact'] & table['evidence_found']).sum()), '/', len(table))
print('추론 지연시간: N/A (mock)')
