# Day29 · 01 · AI Agent vs 고정 RAG/Workflow · 기본필수 리뷰

## 1. 구현 내역 (`tasks.py`)
- `classify_request(question: str) -> str`:
  - 빈 문자열 또는 비문자열 입력 시 `ValueError`를 발생시켜 비정상 입력을 차단합니다.
  - 문서 검색 성격 키워드(`_RAG_KEYWORDS`)와 DB 상태 조회 성격 키워드(`_DB_KEYWORDS`)를 판별하여, 두 성격이 모두 포함되면 `'agent'`, DB 상태 조회만 해당하면 `'db'`, 그 외 일반 문서 질의는 `'rag'`를 반환합니다.
- `plan_for_request(question: str) -> dict`:
  - `classify_request`로 결정된 전략에 따라 `rag_search`, `lookup_status` 중 필요한 Tool 목록을 매핑하여 `{"strategy": ..., "tools": ...}` 형태로 반환합니다.

## 2. 검증 결과
- 구조 점검 (`python 01_basic/01_agent_vs_rag/main.py --check`):
  - `TODO 함수: ['classify_request', 'plan_for_request']` 정상 출력 확인
- 오프라인 계약 테스트 (`pytest tests/test_contracts.py -k test_01_basic_01_agent_vs_rag -v`):
  - `1 passed` 통과
- 실제 DB 연동 실행 (`python 01_basic/01_agent_vs_rag/main.py`):
  - `20261126/mentee/.env` 미설정으로 `RuntimeError: DATABASE_URL을 .env에 지정하세요. 기존 report_agent_lab 접속 문자열이 필요합니다.` 발생 (새 노트북 PostgreSQL 비밀번호 일치, `pgvector` 설치 및 `report_agent_lab` DB 준비 후 재실행 필요).

## 3. 학습 기록 (요약)
1. 고정 RAG는 비정형 문서 원문(`report_read_view`) 검색에 강점이 있고, DB 상태 조회(`reports`)는 `index_status`, `revision` 같은 실시간 정형 상태를 정확히 확인하는 데 필요합니다.
2. 문서 근거와 DB 상태가 함께 필요한 복합 질의에서는 단일 파이프라인 대신 두 Tool(`rag_search`, `lookup_status`)을 조합하는 Agent 전략이 적합합니다.
3. `plan_for_request`처럼 조건문으로 Tool 목록을 정하는 것은 사전 라우팅 계획일 뿐, 실제 LLM이 Tool Call을 선택하고 `ToolMessage` 결과를 받아 다음 행동을 결정하는 Agent 루프와는 구분됩니다.
