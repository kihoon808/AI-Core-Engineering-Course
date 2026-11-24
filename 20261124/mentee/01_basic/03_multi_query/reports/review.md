# 실행 기록 (직접 작성)

- 선택 단계 / 실습: 기본필수 / Day27 실습 03 (03_multi_query)
- 실행 날짜와 Python Interpreter: 2026-11-24 / `c:\Projects\Workspace\.venv\Scripts\python.exe` (Python 3.13.14)
- 실행 모드: offline_fixture (`offline_fixture`, 고정 검색 Fixture 사용)
- 요청 질문과 Category: Q01 ("회의실 예약을 취소하는 방법은?") / 시설
- Query Rewrite의 원 질문과 검색용 질문:
  - 원 질문: "회의실 예약을 취소하는 방법은?"
  - 확장 질문: "회의실 예약 철회는 어떻게 하나요?", "회의실 예약 취소 조건은?", "회의실 사용 후 청소"
- Candidate ID -> Rerank ID -> Context included ID:
  - 개별 질문별 5개씩 검색된 결과를 `chunk_id` 기준으로 통합해 중복 없는 8개 후보(`FAC-102-C1`, `FAC-103-C1`, `FAC-104-C1`, `FAC-105-C1`, `FAC-109-C1`, `FAC-107-C1`, `FAC-108-C1`, `FAC-101-C1`)로 병합
- 답변과 출처 문서의 실제 내용 대조:
  - `found_by_query` 메타데이터에 각 청크를 찾아낸 질문 목록이 정상 추적됨 (`FAC-102-C1`은 4개 질문 모두에서 검색됨).
- 실패 또는 예상과 다른 결과: 없음 (`pytest` 1개 테스트 통과)
- 고친 TODO와 이유:
  - `D27-03-B01` (`plan_queries`): 원 질문을 첫 번째로 유지하면서 `extras`와 중복 제거 결합.
  - `D27-03-B02` (`merge_candidates`): `chunk_id` 기준 중복 제거 및 `metadata['found_by_query']` 기록.
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): 다중 질문으로 확장된 후보를 후속 Reranking 단계에 전달했을 때 단일 질문 대비 정답 포함률(Recall)이 개선되는지 실측 필요.
