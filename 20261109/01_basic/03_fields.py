"""
OCR로 인식된 텍스트 원문에서 핵심 정보(날짜, 업체명, 총금액)를 추출합니다.
정규식(Regex)을 이용해 특정 라벨 키워드 뒤에 오는 원하는 값만 정확히 가져옵니다.
추출된 필드는 구조화된 JSON 데이터로 저장합니다.
"""
from pathlib import Path
import json
import re

base = Path(__file__).resolve().parent
docs = json.loads((base / 'lesson.json').read_text(encoding='utf-8'))['documents']
records = []
for name in ['doc01', 'doc02', 'doc03']:
    text = docs[name]['ocr']['text']
    # DATE 줄 뒤의 날짜 부분을 추출합니다. OCR 원문도 함께 보존합니다.
# TODO B03
    # 정규표현식으로 DATE: 라벨 뒷부분의 날짜 문자열을 매칭하여 추출합니다.
    issued_at = re.search(r'^DATE: (.+)$', text, re.MULTILINE).group(1)
# TODO 끝 B03
    # 정규표현식으로 SUPPLIER: 라벨 뒤 공급업체 이름을 추출합니다.
    supplier = re.search(r'^SUPPLIER: (.+)$', text, re.MULTILINE).group(1)
# TODO B04
    # TOTAL: 라벨 뒤에 위치한 최종 금액 숫자만 찾아 정수형(int)으로 변환합니다.
    total_amount = int(re.search(r'^TOTAL: (\d+)$', text, re.MULTILINE).group(1))
# TODO 끝 B04
    records.append({'document_id': name, 'issued_at': issued_at, 'supplier': supplier, 'total_amount': total_amount, 'currency': 'KRW', 'ocr_source': 'recorded Tesseract', 'raw_text': text})
    print(name, issued_at, supplier, total_amount)
(base / 'p03_fields.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
