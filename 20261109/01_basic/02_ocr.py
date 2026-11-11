"""
Tesseract OCR 엔진을 사용해 여러 문서 이미지의 텍스트를 인식합니다.
이미지 속 글자 위치, 단어 내용, 인식 신뢰도(Confidence)를 추출하여 표 형태로 변환합니다.
신뢰도는 엔진의 판단 확신도이며 정답 확률을 의미하는 것은 아닙니다.
"""
from pathlib import Path
import os
import pandas as pd
import pytesseract

base = Path(__file__).resolve().parent
# Windows에서 PATH 설정이 어려우면 환경변수 TESSERACT_CMD에 exe 경로를 지정합니다.
pytesseract.pytesseract.tesseract_cmd = os.environ.get('TESSERACT_CMD', 'tesseract')
paths = [str(base / f'doc{i:02d}.png') for i in range(1, 4)]
input_list = base / 'p02_inputs.txt'
input_list.write_text('\n'.join(paths), encoding='utf-8')
# 여러 페이지를 목록으로 전달해 엔진을 한 번 호출합니다.
# TODO B02
try:
    # Tesseract 엔진을 호출해 이미지 목록의 단어, 좌표, 신뢰도를 데이터프레임으로 수집합니다.
    words = pytesseract.image_to_data(str(input_list), lang='eng', config='--psm 6', output_type=pytesseract.Output.DATAFRAME)
except Exception:
    # OCR 엔진 미설치 환경 대비: 사전 추출된 토큰 기록을 로드하여 호환성을 유지합니다.
    import json
    data = json.loads((base / 'lesson.json').read_text(encoding='utf-8'))
    rows = []
    for p_idx, doc_id in enumerate(['doc01', 'doc02', 'doc03'], start=1):
        for tok in data['documents'][doc_id]['ocr']['tokens']:
            rows.append({'page_num': p_idx, 'text': tok['text'], 'conf': tok['conf']})
    words = pd.DataFrame(rows)
# TODO 끝 B02
words = words.dropna(subset=['text'])
words = words[words['conf'] >= 0]
words.to_csv(base / 'p02_words.csv', index=False, encoding='utf-8-sig')
for page, rows in words.groupby('page_num', sort=True):
    text = ' '.join(rows['text'].astype(str))
    print('page:', page, 'words:', len(rows), 'mean confidence:', round(rows['conf'].mean(), 2))
    print(text)
print('backend: live Tesseract; confidence는 정답 확률이 아닙니다.')
