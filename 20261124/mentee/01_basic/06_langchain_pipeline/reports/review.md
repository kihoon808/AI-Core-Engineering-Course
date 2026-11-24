# 실행 기록 (직접 작성)

- 선택 단계 / 실습: 기본필수 / Day27 실습 06 (06_langchain_pipeline)
- 실행 날짜와 Python Interpreter: 2026-11-24 / `c:\Projects\Workspace\.venv\Scripts\python.exe` (Python 3.13.14)
- 실행 모드: offline_fixture (`offline_fixture`, 교육용 고정 응답 및 Fixture 검색 사용)
- 요청 질문과 Category: Q02 ("그럼 취소는 어떻게 해?") / 시설
- Query Rewrite의 원 질문과 검색용 질문:
  - 원 질문 (`original_question`): "그럼 취소는 어떻게 해?"
  - 검색용 질문 (`search_query`): "회의실 예약을 취소하는 방법은?"
- Candidate ID -> Rerank ID -> Context included ID:
  - Candidate/Rerank: `['FAC-102-C1', 'FAC-103-C1', 'FAC-104-C1', 'FAC-105-C1', 'FAC-109-C1']`
  - Context included: `['FAC-102-C1', 'FAC-103-C1']`
- 답변과 출처 문서의 실제 내용 대조:
  - 응답: `[교육용 고정 응답] 회의실 예약을 취소하려면 예약 시스템의 나의 예약 메뉴에서 취소를 선택합니다. 시작 2시간 전까지 취소할 수 있습니다.`
  - `source_ids`: `[1002]` -> `sources[0].citation_id = 1002` (`FAC-102-C1`)와 정상 연결됨.
- 실패 또는 예상과 다른 결과: 초기 구현 시 `RagRequest` 스키마(`query` 필수, `extra='forbid'`)와 불일치해 `ValidationError` 발생 -> `question`을 `query`로 수정하고 불필요한 `role` 제거 후 통과.
- 고친 TODO와 이유:
  - `D27-06-B01` (`prepare_pipeline_request`): `RagRequest` 스키마에 맞춰 `query`, `history`, `category` 반환.
  - `D27-06-B02` (`wire_langchain_pipeline`): `create_rag_pipeline(*dependencies, offline=offline)`로 LCEL 체인 조립.
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): 실제 LLM/DB 연결 모드에서도 `trace.original_question` 보존 및 `citation_id` 매핑이 유지되는지 검증 필요.
