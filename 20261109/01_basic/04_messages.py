"""
시각 언어 모델(VLM)에 입력할 멀티모달 대화 메시지 구조를 구성합니다.
이미지 파일 경로와 질문 텍스트를 담은 표준 프롬프트 규격을 정의합니다.
실제 모델 추론 대신 교육용 모의(Mock) 응답을 매핑하여 파이프라인 구조를 확인합니다.
"""
from pathlib import Path
import json

base = Path(__file__).resolve().parent
lesson = json.loads((base / 'lesson.json').read_text(encoding='utf-8'))
doc = lesson['documents']['doc01']
rows = []
for answer in doc['mock_vlm']['responses']:
    question = lesson['questions'][answer['field']]
# TODO B05
    # 사용자(user) 역할로 이미지 경로와 질문 텍스트를 content 리스트에 구성합니다.
    messages = [{'role': 'user', 'content': [{'image': doc['file']}, {'text': question}]}]
# TODO 끝 B05
    rows.append({'backend': 'mock', 'messages': messages, 'response': answer, 'model_id': None, 'inference_ms': None})
    print(question, '->', answer['answer'])
(base / 'p04_mock_answers.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
print('MOCK: 교사가 작성한 응답 예시입니다. 실제 모델 출력이 아닙니다.')
