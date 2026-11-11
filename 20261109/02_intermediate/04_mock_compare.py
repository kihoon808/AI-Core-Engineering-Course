"""
VLM 모의 응답이 제시한 근거(Evidence) 문자열이 실제 OCR 원문에 존재하는지 검증합니다.
답변의 그라운딩(문서 내 실제 근거 유무)을 점검하여 환각(Hallucination) 가능성을 스크리닝합니다.
근거가 확인되지 않는 필드는 추가 검토(review) 플래그를 설정하여 사후 감사에 활용합니다.
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
    for answer in doc['mock_vlm']['responses']:
        # 문자열 포함 검사는 1차 점검일 뿐 의미상 올바른 답임을 증명하지 않습니다.
# TODO A04
        # 응답에 제시된 근거(evidence) 문자열이 현재 문서의 OCR 원문에 존재하는지 확인합니다.
        evidence_found = bool(answer.get('evidence') and answer['evidence'] in doc['ocr']['text'])
# TODO 끝 A04
        rows.append({'document_id':name, 'backend':'mock', **answer, 'evidence_found':evidence_found, 'review':not evidence_found})
table = pd.DataFrame(rows)
table.to_csv(out / 'p04_mock_review.csv', index=False, encoding='utf-8-sig')
print('mock 필드:', len(table), '근거 문자열 발견:', int(table['evidence_found'].sum()))
print('모의 응답의 평가 연습이며 실제 VLM 정확도가 아닙니다.')
