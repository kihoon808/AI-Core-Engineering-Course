# 실행 기록 (직접 작성)

- 선택 단계 / 실습: 심화(Advanced) / Day27 실습 06 (06_langchain_pipeline)
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
  - `trace_check` 통과 및 `audit`에서 `total_ms=2.48`, `source_ids_linked=true`, `grounding_verified=false`(구조 연결만 확인, 진위 판단 분리) 기록 확인.
- 실패 또는 예상과 다른 결과: 없음 (`pytest` 1개 테스트 통과)
- 고친 TODO와 이유:
  - `D27-06-A01` (`schemas/request.py`), `D27-06-A02` (`chains/graph.py`), `D27-06-A03` (`services/trace.py`), `D27-06-A04` (`services/audit.py`) 계층별 역할 분리 구현.
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): 실제 GPU/DB/LLM 경로에서 각 Stage별 `timing_ms` 병목(특히 Rerank vs Retrieval)을 측정해 최적화 대상 식별 필요.
