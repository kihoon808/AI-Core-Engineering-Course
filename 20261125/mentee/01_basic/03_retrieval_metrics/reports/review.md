# 수행 기록 · Day28 실습 03

**실행한 모드:** `offline_fixture` (`python 01_basic/03_retrieval_metrics/main.py --offline`, pytest `2 passed in 0.13s`)

**작성 TODO:** `calculate_recall`, `count_gold_hits`

## 1. 질문·입력
- 어떤 `question_id`를 사용했는가?
  - `Q01`, `Q07`, `Q06`을 사용했습니다. (`dataset_version`: `d28-eval-v1`)
- Gold Label을 Target 입력에 전달하지 않았는가?
  - 네. `target_inputs(qby[qid])`만 `target_fixture`에 전달하여 검색 결과(`ranked_ids`)를 얻은 뒤, 평가 단계에서만 `gold[qid]`와 비교했습니다.

## 2. 실제 확인한 출력
- 결과 JSON과 핵심 점수·출처 ID:
  - `Q01`: `gold_count=1`, `hits_at_3=1`, `recall_at_3=1.0` (`FAC-102-C1`가 3위에 포함)
  - `Q07`: `gold_count=2`, `hits_at_3=1`, `recall_at_3=0.5` (Gold 2개 중 `FAC-102-C1`만 2위에 포함, `FAC-104-C1`은 4위로 Top-3 밖)
  - `Q06`: `gold_count=0`, `hits_at_3=0`, `recall_at_3=null` (No-answer 질문)
- No-answer / 실패 / 정상의 차이:
  - `Q06`은 Gold가 없는 무정답 질문이므로 `recall_at_3`을 `0.0`이 아닌 `null`(`None`)로 반환하여 전체 평균 Recall 왜곡을 방지합니다.

## 3. 해설
- 왜 이 공식 또는 분기 조건이 필요한가?
  - `Recall@k`는 Top-k 내에 정답 문서를 얼마나 빠짐없이 가져왔는지 측정하며, 중복 ID를 제거(`set` 교집합)해야 동일 문서 중복 반환으로 점수가 부풀려지는 것을 막을 수 있습니다.
- 평가 결과가 좋지 않다면 다음에 수정할 모듈은 어디인가?
  - `Recall@k`가 낮다면 1차 Retriever(임베딩 모델, BM25/Dense 하이브리드, 청킹 크기, `top_k` 확장)를 우선 개선해야 합니다.

## 4. 11월 26일 Agent와 연결
- Agent가 이 RAG 검색 Tool을 사용하기 전에 추가로 확인해야 할 것은 무엇인가?
  - 검색 결과 Top-k에 포함된 문서의 출처(Citation), 접근 권한(RBAC), 그리고 검색 결과가 비어 있을 때의 Fallback/재질의 정책을 확인해야 합니다.
