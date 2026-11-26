# Day29 · 02 · AIMessage.tool_calls / ToolMessage · 기본필수 리뷰

## 1. 구현 내역 (`tasks.py`)
- `make_request(tool_name: str, args: dict, call_id: str) -> dict`:
  - 허용된 Tool 이름(`rag_search`, `lookup_status`), `dict` 타입 인수, 비어 있지 않은 `call_id`를 검증한 뒤 `{"name": ..., "args": ..., "id": ...}` 형태의 요청 딕셔너리를 생성합니다.
- `match_result(call: dict, result: dict) -> dict`:
  - 요청의 `id` 포함 여부와 결과 `dict` 타입을 검증하고, 요청의 `id`를 `tool_call_id`로 연결한 `{"type": "ToolMessage", "tool_call_id": ..., "name": ..., "content": ...}` 구조를 반환합니다.

## 2. 검증 결과
- 구조 점검 (`python 01_basic/02_tool_message/main.py --check`):
  - `TODO 함수: ['make_request', 'match_result']` 정상 출력 확인
- 오프라인 계약 테스트 (`pytest tests/test_contracts.py -k test_01_basic_02_tool_message -v`):
  - `1 passed` (0.11s) 통과
- 실제 DB 연동 실행 (`python 01_basic/02_tool_message/main.py`):
  - `20261126/mentee/.env` 미설정으로 `RuntimeError: DATABASE_URL을 .env에 지정하세요. 기존 report_agent_lab 접속 문자열이 필요합니다.` 발생 (DB 설정 완료 후 재실행 필요).

## 3. 학습 기록 (요약)
1. `AIMessage.tool_calls`는 모델이 어떤 도구를 어떤 인수로 호출할지 제안하는 요청(`name`, `args`, `id`)일 뿐, 실제 실행이나 DB 조회를 의미하지 않습니다.
2. 실제 도구를 실행하고 DB 결과를 반환하는 주체는 Python 애플리케이션이며, 그 결과를 `ToolMessage` 형태로 포장해 모델에 다시 전달해야 합니다.
3. 여러 도구가 동시에 또는 순차적으로 호출될 때 각 요청과 응답을 정확히 짝짓는 연결 키가 `id`와 `tool_call_id`입니다.
