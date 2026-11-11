"""
문서 이미지 전처리, OCR 기록 파싱, 정형 데이터 저장을 아우르는 미니 파이프라인입니다.
흑백 변환 및 Otsu 이진화 전처리를 수행하고, OCR 원문 텍스트에서 주요 필드를 추출합니다.
추출된 필드 정보와 원문 메타데이터를 통합하여 JSON 파일로 최종 저장합니다.
"""
from pathlib import Path
import os
import json
import re
import cv2

base = Path(__file__).resolve().parent
# Windows 한글 경로 인식 오류를 방지하기 위해 작업 디렉토리를 변경합니다.
os.chdir(base)

lesson = json.loads((base / 'lesson.json').read_text(encoding='utf-8'))
records = []
for name in ['doc01', 'doc02', 'doc03']:
    # 상대 경로로 안전하게 이미지를 로드합니다.
    image = cv2.imread(f'{name}.png')
# TODO B08
    # BGR 컬러 이미지를 그레이스케일(흑백 단일 채널)로 변환합니다.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# TODO 끝 B08
    # Otsu 알고리즘으로 최적 임계값을 계산하여 이진화(흑/백) 이미지를 생성합니다.
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite(f'p07_{name}_binary.png', binary)
    # 이 기록은 원본 이미지로 실제 추론한 결과입니다. 방금 만든 binary의 추론 결과가 아닙니다.
    text = lesson['documents'][name]['ocr']['text']
    fields = {'issued_at': re.search(r'DATE: (\d{4}-\d{2}-\d{2})', text).group(1), 'supplier': re.search(r'SUPPLIER: (.+)', text).group(1), 'total_amount': int(re.search(r'TOTAL: (\d+)', text).group(1))}
    records.append({'document_id': name, 'fields': fields, 'raw_text': text, 'ocr_backend': 'recorded_tesseract_on_original', 'vlm_backend': 'not_used'})
    print(name, fields)
# TODO B09
# 추출된 전체 레코드를 UTF-8 형식의 들여쓰기된 JSON 파일로 저장합니다.
(base / 'p07_documents.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
# TODO 끝 B09
print('문서:', len(records), '/ 이진화 PNG 3개 + 최종 JSON 1개')
