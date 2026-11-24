# 실행 기록 (직접 작성)

- 선택 단계 / 실습: 기본필수 / Day27 실습 05 (05_cross_encoder_reranking)
- 실행 날짜와 Python Interpreter: 2026-11-24 / `c:\Projects\Workspace\.venv\Scripts\python.exe` (Python 3.13.14)
- 실행 모드: offline_fixture (`offline_fixture`, 교육용 고정 점수 `fixed_rank_scores` 사용)
- 요청 질문과 Category: Q01 ("회의실 예약을 취소하는 방법은?") / 시설
- Query Rewrite의 원 질문과 검색용 질문: 해당 없음
- Candidate ID -> Rerank ID -> Context included ID:
  - Before: `['FAC-101-C1', 'FAC-107-C1', 'FAC-102-C1', 'FAC-103-C1', 'FAC-104-C1']`
  - After: `['FAC-102-C1', 'FAC-103-C1', 'FAC-104-C1', 'FAC-101-C1', 'FAC-107-C1']`
  - Rerank Scores: `[3.2, 2.6, 2.1, 0.5, 0.3]`
- 답변과 출처 문서의 실제 내용 대조:
  - 초기 Top-2 밖에 있던 `FAC-102-C1`, `FAC-103-C1`이 Reranking 후 1, 2위로 상승함. `after_ids`는 `before_ids`의 순열(동일 후보 집합)임.
- 실패 또는 예상과 다른 결과: 없음 (`pytest` 1개 테스트 통과)
- 고친 TODO와 이유:
  - `D27-05-B01` (`create_pairs`): CrossEncoder 입력 형식인 `[질문, 문서본문]` 쌍 목록 생성.
  - `D27-05-B02` (`rank_documents`): `scorer` 점수를 `metadata['rerank_score']`에 저장하고 내림차순 정렬.
- 다음 개선 가설 (실측 전에 성공으로 단정하지 말 것): `--offline` 고정 점수가 아닌 실제 GPU CrossEncoder 추론 시의 순위 변동 및 레이턴시 실측 필요.
