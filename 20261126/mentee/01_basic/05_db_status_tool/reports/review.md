# Day29 · 05 · PostgreSQL Read-only lookup_status · 기본필수 리뷰

## 1. 구현 내역 (`tasks.py`)
- `parse_report_id(value) -> int`:
  - `bool`, 소수, 음수, 0, 선행 0이 포함된 문자열 등을 거절하고 1 이상의 정수 `report_id`만 반환합니다.
- `status_view(raw: dict) -> dict`:
  - `index_status`(`pending`/`ready`/`failed`)와 실제 벡터 최신성(`vector_fresh`)을 구분해 반환하고, 두 조건이 모두 충족될 때만 `ready_for_rag=True`로 판정합니다.

## 2. 검증 결과
- 구조 점검 (`python 01_basic/05_db_status_tool/main.py --check`):
  - `TODO 함수: ['parse_report_id', 'status_view']` 정상 출력 확인
- 오프라인 계약 테스트 (`pytest tests/test_contracts.py -k test_01_basic_05_db_status_tool -v`):
  - `1 passed` 통과
- 실제 DB 연동 실행 (`python 01_basic/05_db_status_tool/main.py`):
  - `20261126/mentee/.env` 내 `DATABASE_URL` 미설정으로 `RuntimeError: DATABASE_URL을 .env에 지정하세요. 기존 report_agent_lab 접속 문자열이 필요합니다.` 발생.

## 3. 학습 기록 (요약)
1. `lookup_status` Tool은 `task_id`가 아니라 `reports.report_id`를 양의 정수로 엄격히 검증해 읽기 전용 `SELECT` 조회만 수행합니다.
2. DB의 `index_status`가 `ready`로 표시되어 있더라도 실제 임베딩 벡터의 최신성(`vector_fresh`)이 `False`일 수 있으므로 두 값을 분리해 확인해야 합니다.
3. 입력 검증과 상태 해석 로직을 순수 함수로 분리하면 DB 연결 전에도 오프라인 계약 테스트로 안전하게 검증할 수 있습니다.
