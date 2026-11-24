# 실행 기록 (직접 작성)

- 선택 단계 / 실습: 중급(Intermediate) / Day27 실습 06 (06_langchain_pipeline)
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
  - `trace_check`: `has_original_question=true`, `has_search_query=true`, `candidate_count=5`, `included_count=2`, `included_subset_of_candidates=true` 확인.
- 실패 또는 예상과 다른 결과: 없음 (`pytest` 1개 테스트 통과)
- 고친 TODO와 이유:
  - `D27-06-I01` (`steps.py` `prepare_pipeline_request`): `RagRequest` 스키마에 맞춰 `query`, `history`, `category` 전달.
  - `D27-06-I02` (`steps.py` `wire_langchain_pipeline`): `create_rag_pipeline`으로 LCEL 체인 조립.
  - `D27-06-I03` (`checks.py` `validate_trace`): `trace` 내 원 질문, 검색 질문, 후보 및 Context 포함 여부 검증.
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): 실제 LLM 환경에서 `search_query`가 `original_question`과 달라질 때도 `included_subset_of_candidates`가 항상 참인지 확인 필요.
