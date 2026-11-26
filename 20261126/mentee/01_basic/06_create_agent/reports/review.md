# Day29 · 06 · create_agent + 실제 Tool 2개 · 기본필수 리뷰

## 1. 구현 내역 (`tasks.py`)
- `question_for_agent(report_id: int) -> str`:
  - `report_id`(1 이상 정수)를 검증한 뒤 문서 검색(`rag_search`)과 해당 보고서 인덱싱 상태 조회(`lookup_status`)를 모두 요구하는 복합 질문을 생성합니다.
- `make_agent()`:
  - `coursekit.agent.build_agent()`를 호출해 `rag_search`, `lookup_status` Tool 2개와 `ToolCallLimitMiddleware`, `ModelCallLimitMiddleware`가 적용된 LangChain Agent를 반환합니다.

## 2. 검증 결과
- 구조 점검 (`python 01_basic/06_create_agent/main.py --check`):
  - `TODO 함수: ['make_agent', 'question_for_agent']` 정상 출력 확인
- 오프라인 계약 테스트 (`pytest tests/test_contracts.py -k test_01_basic_06_create_agent -v`):
  - `1 passed` 통과
- 실제 Agent 연동 실행 (`python 01_basic/06_create_agent/main.py`):
  - `20261126/mentee/.env` 내 `DATABASE_URL` 미설정으로 `RuntimeError: DATABASE_URL을 .env에 지정하세요. 기존 report_agent_lab 접속 문자열이 필요합니다.` 발생.

## 3. 학습 기록 (요약)
1. `create_agent`는 `rag_search`와 `lookup_status` 두 Tool을 모델에 바인딩해 질문 성격에 따라 모델이 자율적으로 0개, 1개 또는 복수 Tool을 호출하게 합니다.
2. `ToolCallLimitMiddleware`와 `ModelCallLimitMiddleware`를 함께 설정해 무한 루프나 과도한 API/DB 호출을 방지할 수 있습니다.
3. `make_agent` 내부에서 `coursekit.agent`를 지연 임포트하면 오프라인 단위 테스트 시 `.env`나 LLM 설정 없이도 `question_for_agent` 계약을 검증할 수 있습니다.
