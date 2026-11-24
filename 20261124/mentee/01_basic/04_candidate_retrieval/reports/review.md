# 실행 기록 (직접 작성)

- 선택 단계 / 실습: 기본필수 / Day27 실습 04 (04_candidate_retrieval)
- 실행 날짜와 Python Interpreter: 2026-11-24 / `c:\Projects\Workspace\.venv\Scripts\python.exe` (Python 3.13.14)
- 실행 모드: offline_fixture (`offline_fixture`, 고정 검색 Fixture 사용)
- 요청 질문과 Category: Q01 ("회의실 예약을 취소하는 방법은?") / 시설
- Query Rewrite의 원 질문과 검색용 질문: 해당 없음 (단일 질문으로 후보 검색 수행)
- Candidate ID -> Rerank ID -> Context included ID:
  - `candidate_k=10`, `context_k=3`으로 요청하여 9개 후보(`FAC-102-C1`, `FAC-103-C1`, `FAC-104-C1`, `FAC-105-C1`, `FAC-109-C1`, `FAC-108-C1`, `FAC-107-C1`, `FAC-101-C1`, `FAC-106-C1`) 조회
- 답변과 출처 문서의 실제 내용 대조:
  - `candidate_k >= context_k` 조건을 충족하며, `RunnableLambda.invoke()`를 통해 후보 `Document` 리스트를 정상 반환함.
- 실패 또는 예상과 다른 결과: 없음 (`pytest` 1개 테스트 통과)
- 고친 TODO와 이유:
  - `D27-04-B01` (`make_candidate_request`): `candidate_k`(10)와 `context_k`(3)를 분리해 후속 Reranking 여유 확보.
  - `D27-04-B02` (`fetch_documents`): `retriever.invoke(payload)`로 `Runnable` 인터페이스 호출.
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): `candidate_k`를 늘릴수록 Recall은 올라가지만 Reranking 지연 시간도 증가하므로 최적의 `candidate_k` 임계값 측정 필요.
