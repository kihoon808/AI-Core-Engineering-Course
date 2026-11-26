# Day29 · 08 · FastAPI -> Agent -> Tool -> 응답 · 기본필수 리뷰

## 1. 구현 내역 (`tasks.py`)
- `default_question() -> str`:
  - 보고서 내용 검색과 보고서 63번의 인덱싱 상태 조회를 동시에 요구하는 표준 질의를 반환합니다.
- `api_response(run: dict) -> dict`:
  - Agent 실행 결과에서 `status`, `answer`, `citation_ids_valid`, `verified_evidence_ids`, `tool_trace`를 분리해 API 응답 계약으로 변환합니다.
  - `citation_ids_valid`가 `False`이면 응답 `status`를 `citation_validation_failed`로 전환하고, 로컬 전용 무인증 범위(`auth_scope: "local_only_no_user_auth"`)를 명시합니다.

## 2. 검증 결과
- 구조 점검 (`python 01_basic/08_end_to_end/main.py --check`):
  - `TODO 함수: ['api_response', 'default_question']` 정상 출력 확인
- 오프라인 계약 테스트 (`pytest tests/test_contracts.py -k "test_01_basic_" -v`):
  - `01_basic` 01에서 08까지 8개 전체 통과 (`8 passed in 0.21s`)
- 실제 Agent 연동 실행 (`python 01_basic/08_end_to_end/main.py`):
  - `20261126/mentee/.env` 내 `DATABASE_URL` 미설정으로 `RuntimeError: DATABASE_URL을 .env에 지정하세요. 기존 report_agent_lab 접속 문자열이 필요합니다.` 발생.

## 3. 학습 기록 (요약)
1. FastAPI 엔드포인트는 Agent의 원시 메시지 목록을 그대로 노출하지 않고, 최종 답변(`answer`)·실행 추적(`tool_trace`)·출처 검증 결과(`citation_ids_valid`)를 구조화된 계약으로 변환해 반환해야 합니다.
2. 모델이 생성한 답변에 검증된 Context 외부의 출처 ID가 섞여 있을 경우 응답 상태를 실패(`citation_validation_failed`)로 분리해 신뢰할 수 없는 인용을 차단합니다.
3. 로컬 실습용 API에 사용자 인증/ACL이 구현되어 있지 않음을 응답 계약(`auth_scope`)에 명시해 운영 보안 경계와 혼동하지 않도록 합니다.
