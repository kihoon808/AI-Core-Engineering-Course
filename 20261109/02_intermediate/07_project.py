"""
OCR 추출 결과와 VLM 모의 응답을 결합한 하이브리드(Hybrid) 문서 처리 파이프라인입니다.
이진화 전처리 및 OCR 정규식 파싱을 거친 후, VLM 응답과의 값 일치 및 근거(Evidence) 유무를 검증합니다.
불일치하거나 근거가 없는 경우 수동 검토(review=True) 플래그를 부여하여 데이터 신뢰성을 보장합니다.
"""
from pathlib import Path
import os
import json
import re
import numpy as np
import pandas as pd
import cv2

base = Path(__file__).resolve().parent
# Windows 한글 경로 디코딩 오류 방지를 위해 작업 디렉토리를 변경합니다.
os.chdir(base)

data = base / 'data'
out = base / 'outputs'
out.mkdir(exist_ok=True)
lesson = json.loads((data / 'lesson.json').read_text(encoding='utf-8'))

results = []
for name, doc in lesson['documents'].items():
    # 상대 경로로 안전하게 이미지를 로드합니다.
    image = cv2.imread(f"data/{doc['file']}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(f"outputs/{name}_binary.png", binary)
    text = doc['ocr']['text']
# TODO A07
    # OCR 원문에서 정규표현식을 통해 세 필드(발행일, 공급업체, 총금액)를 추출합니다.
    fields = {
        'issued_at': re.search(r'DATE: (\d{4}-\d{2}-\d{2})', text).group(1),
        'supplier': re.search(r'SUPPLIER: (.+)', text).group(1),
        'total_amount': int(re.search(r'TOTAL: (\d+)', text).group(1))
    }
# TODO 끝 A07
    for response in doc['mock_vlm']['responses']:
# TODO A08
        # OCR 값과 VLM 답변이 불일치하거나 원문 내 근거 문자열이 누락된 경우 재검토(review=True)로 마킹합니다.
        diff = bool(fields[response['field']] != response['answer'])
        no_evidence = not bool(response.get('evidence') and response['evidence'] in text)
        review = bool(diff or no_evidence)
# TODO 끝 A08
        results.append({'document_id':name, 'field':response['field'], 'ocr_value':fields[response['field']], 'vlm_answer':response['answer'], 'evidence':response['evidence'], 'review':review, 'ocr_backend':'recorded_tesseract', 'vlm_backend':'mock'})
(out / 'final_fields.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
pd.DataFrame(results).to_csv(out / 'review.csv', index=False, encoding='utf-8-sig')
print('문서:', len(lesson['documents']), '필드:', len(results), '검토:', sum(r['review'] for r in results))
print('정답 파일은 추출·검토 판단에 사용하지 않았습니다.')
