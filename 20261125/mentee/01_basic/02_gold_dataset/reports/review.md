# 수행 기록 · Day28 실습 02

**실행한 모드:** `offline_fixture` (`python 01_basic/02_gold_dataset/main.py --offline`, pytest `2 passed in 0.16s`)

**작성 TODO:** `select_gold`, `validate_gold_ids`

## 1. 질문·입력
- 어떤 `question_id`를 사용했는가?
  - `Q01`, `Q05`, `Q06`, `Q07`을 사용했습니다. (`dataset_version`: `d28-eval-v1`)
- Gold Label을 Target 입력에 전달하지 않았는가?
  - 네. `result.json`의 `target_example`을 보면 `Q01`에 대해 `question_id`, `question`, `category`, `history`만 포함되며 `gold_chunk_ids`는 포함되지 않았습니다.

## 2. 실제 확인한 출력
- 결과 JSON과 핵심 점수·출처 ID:
  - `Q01`: `gold_chunk_ids=["FAC-102-C1"]`, `valid_ids=true`
  - `Q05`: `gold_chunk_ids=["ACA-101-C1"]`, `valid_ids=true`
  - `Q06`: `gold_chunk_ids=[]`, `valid_ids=true` (무정답 질문)
  - `Q07`: `gold_chunk_ids=["FAC-104-C1", "FAC-102-C1"]`, `valid_ids=true`
- No-answer / 실패 / 정상의 차이:
  - `Q06`은 `gold_chunk_ids`가 빈 리스트(`[]`)인 No-answer 질문이며, `valid_ids`는 `true`로 정상 처리됩니다. 반면 일반 Retrieval 지표 평균 계산 시에는 `Q06`을 Recall 0으로 합산하지 않고 분리해야 합니다.

## 3. 해설
- 왜 이 공식 또는 분기 조건이 필요한가?
  - Gold ID에 중복이 있으면 Recall/Precision 계산이 왜곡되고, `corpus`에 없는 ID가 섞이면 모델이 절대 맞출 수 없는 잘못된 평가셋이 됩니다. 따라서 `set` 길이 비교로 중복을 막고 `corpus` 존재 여부를 사전 검증해야 합니다.
- 평가 결과가 좋지 않다면 다음에 수정할 모듈은 어디인가?
  - `valid_ids`가 `false`라면 데이터셋/청킹 파이프라인(또는 Gold 어노테이션 매핑)을 먼저 수정해야 합니다. `valid_ids`가 `true`인데 검색 지표가 낮다면 Retriever/Reranker 모듈을 개선합니다.

## 4. 11월 26일 Agent와 연결
- Agent가 이 RAG 검색 Tool을 사용하기 전에 추가로 확인해야 할 것은 무엇인가?
  - 문서 청크 ID 체계가 최신 `corpus`와 일치하는지, 무정답(No-answer) 질문에 대해 Agent가 억지 답변 대신 "근거 없음"으로 안전하게 응답하는지, 그리고 문서 접근 권한(RBAC)을 확인해야 합니다.
