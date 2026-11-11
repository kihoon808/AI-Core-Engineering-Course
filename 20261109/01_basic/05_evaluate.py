"""
OCR 필드 추출 결과와 정답(Ground Truth) 라벨을 1:1로 대조하여 정확도를 평가합니다.
각 문서의 날짜, 업체명, 총금액 필드가 정답과 일치하는지 확인합니다.
평가 결과는 CSV 파일로 저장하여 필드별 정확도를 산출합니다.
"""
from pathlib import Path
import json
import re
import pandas as pd

base = Path(__file__).resolve().parent
lesson = json.loads((base / 'lesson.json').read_text(encoding='utf-8'))
rows = []
for name, doc in lesson['documents'].items():
    text = doc['ocr']['text']
    predicted = {'issued_at': re.search(r'DATE: (\d{4}-\d{2}-\d{2})', text).group(1), 'supplier': re.search(r'SUPPLIER: (.+)', text).group(1), 'total_amount': int(re.search(r'TOTAL: (\d+)', text).group(1))}
    for field in ['issued_at', 'supplier', 'total_amount']:
        # ========================================================
        # TODO B06: OCR 추출 결과와 실제 정답 비교
        # ========================================================
        # 추출한 예측값과 정답 데이터(truth)를 비교하여 일치 여부(True/False)를 판별합니다.
        correct = bool(predicted[field] == doc['truth'][field])
        # TODO 끝 B06
        rows.append({'document_id': name, 'field': field, 'predicted': predicted[field], 'correct': correct})
table = pd.DataFrame(rows)
table.to_csv(base / 'p05_field_scores.csv', index=False, encoding='utf-8-sig')
print('문서 수:', len(lesson['documents']), '필드 수:', len(table))
print('필드 일치:', int(table['correct'].sum()), '/', len(table))
print('합성 영어 문서의 기록 비교이며 일반 OCR·한국어 성능이 아닙니다.')
