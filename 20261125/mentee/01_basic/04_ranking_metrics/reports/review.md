# 수행 기록 · Day28 실습 04

**실행한 모드:** `offline_fixture` (`python 01_basic/04_ranking_metrics/main.py --offline`, pytest `2 passed in 0.12s`)

**작성 TODO:** `first_relevant_rank`, `calculate_rr`

## 1. 질문·입력
- 어떤 `question_id`를 사용했는가?
  - `Q01`, `Q07`, `Q06`을 사용했습니다. (`dataset_version`: `d28-eval-v1`)
- Gold Label을 Target 입력에 전달하지 않았는가?
  - 네. `target_inputs(qby[qid])`만 `target_fixture`에 전달해 `ranked_ids`를 생성한 뒤, 평가 단계에서만 `gold[qid]`로 순위를 계산했습니다.

## 2. 실제 확인한 출력
- 결과 JSON과 핵심 점수·출처 ID:
  - `Q01`: `first_rank=3`, `rr_at_3=0.3333333333333333` (1/3)
  - `Q07`: `first_rank=2`, `rr_at_3=0.5` (1/2)
  - `Q06`: `first_rank=null`, `rr_at_3=null` (No-answer 질문)
  - 전체 평균 `mrr_at_3=0.41666666666666663` (`Q01`, `Q07`만 평균: `(0.3333... + 0.5) / 2`)
- No-answer / 실패 / 정상의 차이:
  - `Q06`은 Gold가 없는 무정답 질문이므로 `rr_at_3`이 `null`로 처리되어 `MRR@3` 집계에서 제외됩니다. 반면 정답이 있는 질문에서 Top-k 내 찾지 못한 경우에만 `0.0`으로 계산됩니다.

## 3. 해설
- 왜 이 공식 또는 분기 조건이 필요한가?
  - `Recall@k`는 순위를 구분하지 않지만, `RR`/`MRR`은 첫 번째 정답 문서가 얼마나 상위에 배치되었는지(`1 / rank`)를 반영하므로 LLM Context 상단 배치 품질을 평가하는 데 필수적입니다.
- 평가 결과가 좋지 않다면 다음에 수정할 모듈은 어디인가?
  - `Recall@k`는 높은데 `MRR@k`가 낮다면 후보에는 정답이 있으나 순위가 밀린 것이므로 Reranker(Cross-Encoder) 및 스코어링/정렬 로직을 수정해야 합니다.

## 4. 11월 26일 Agent와 연결
- Agent가 이 RAG 검색 Tool을 사용하기 전에 추가로 확인해야 할 것은 무엇인가?
  - 상위 랭킹 문서가 실제 최신·권한 내 문서인지, 그리고 랭킹 점수가 임계치 이하일 때 Agent가 재검색(Query Rewrite) 또는 보류 판단을 내릴 수 있는지 확인해야 합니다.
