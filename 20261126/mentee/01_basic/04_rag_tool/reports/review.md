# Day29 · 04 · 기존 RAG를 rag_search Tool로 · 기본필수 리뷰

## 1. 구현 내역 (`tasks.py`)
- `prepare_search(query: str, category: str = "ALL") -> dict`:
  - `query`가 공백 제외 1에서 500자 사이의 문자열인지 검증합니다.
  - `category`를 대문자로 정규화한 뒤 허용된 6개 카테고리(`EXPERIMENT`, `DAILY_WORK`, `RESEARCH_PLAN`, `DATA_PROCESSING`, `PROMPT`, `MEETING`) 또는 `ALL`에 속하는지 확인합니다.
- `invoke_rag(request: dict) -> dict`:
  - `request`를 `prepare_search`로 재검증한 뒤 `coursekit.rag.rag_answer`를 호출해 기존 PostgreSQL(`report_agent_lab`) pgvector 검색, CUDA E5/CrossEncoder 재정렬, LLM 근거 답변 생성을 수행합니다.

## 2. 검증 결과
- 구조 점검 (`python 01_basic/04_rag_tool/main.py --check`):
  - `TODO 함수: ['invoke_rag', 'prepare_search']` 정상 출력 확인
- 오프라인 계약 테스트 (`pytest tests/test_contracts.py -k test_01_basic_04_rag_tool -v`):
  - `1 passed` (0.03s) 통과
- 실제 DB·GPU 연동 실행 (`python 01_basic/04_rag_tool/main.py`):
  - `20261126/mentee/.env` 내 `DATABASE_URL` 미설정으로 `RuntimeError: DATABASE_URL을 .env에 지정하세요. 기존 report_agent_lab 접속 문자열이 필요합니다.` 발생 (DB 비밀번호 및 `pgvector` 설정 완료 후 재실행 필요).

## 3. 학습 기록 (요약)
1. 기존 RAG 파이프라인을 Agent의 `rag_search` Tool로 감쌀 때는 입력 단계(`prepare_search`)에서 검색어 길이와 허용 카테고리 화이트리스트를 먼저 검증해야 안전합니다.
2. `coursekit.rag.rag_answer`는 `pgvector` 유사도 검색 후 CUDA CrossEncoder 재정렬과 `validate_source_contract`를 거쳐 실제 Context에 포함된 `[RPT-번호]`만 인용하도록 강제합니다.
3. 오프라인 단위 테스트(`test_contracts.py`)와 실제 DB·GPU 연동 실행(`main.py`)을 분리해 두면 외부 환경 설정 전에도 입력 계약과 순수 로직을 먼저 검증할 수 있습니다.
