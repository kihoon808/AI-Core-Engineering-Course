# Day29 · 07 · Tool 실패·권한·반복 상한 · 기본필수 리뷰

## 1. 구현 내역 (`tasks.py`)
- `validate_report_id(value) -> int`:
  - DB 쿼리 실행 전 `bool`, 음수, 0, 소수, 선행 0 문자열 등 잘못된 입력을 `ValueError`로 사전 차단합니다.
- `classify_error(exc: Exception) -> dict`:
  - 예외 유형을 `INVALID_INPUT`, `PERMISSION_DENIED`, `CONNECTION_ERROR`, `INTERNAL_ERROR`로 분류하고, 예외 원문(`str(exc)`)을 그대로 노출하지 않아 비밀정보·SQL 원문 유출을 방지합니다.

## 2. 검증 결과
- 구조 점검 (`python 01_basic/07_reliability/main.py --check`):
  - `TODO 함수: ['classify_error', 'validate_report_id']` 정상 출력 확인
- 오프라인 계약 테스트 (`pytest tests/test_contracts.py -k test_01_basic_07_reliability -v`):
  - `1 passed` (0.05s) 통과
- 실제 DB 연동 실행 (`python 01_basic/07_reliability/main.py`):
  - `20261126/mentee/.env` 내 `DATABASE_URL` 미설정으로 `RuntimeError: DATABASE_URL을 .env에 지정하세요. 기존 report_agent_lab 접속 문자열이 필요합니다.` 발생.

## 3. 학습 기록 (요약)
1. 잘못된 Tool 인자는 DB 쿼리나 외부 API 호출 전에 애플리케이션 계층(`validate_report_id`)에서 먼저 차단해야 불필요한 부하를 막을 수 있습니다.
2. 오류 응답이나 로그에는 예외 객체의 원문 문자열(`str(exc)`) 대신 정제된 `error_code`와 안전 메시지만 남겨 접속 정보나 SQL 구문 노출을 방지해야 합니다.
3. 입력 오류(`retryable=False`)와 일시적 연결 오류(`retryable=True`)를 구분하면 Agent나 호출자가 재시도 여부를 일관되게 판단할 수 있습니다.
