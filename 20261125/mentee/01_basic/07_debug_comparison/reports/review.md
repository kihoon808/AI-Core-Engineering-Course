# 수행 기록 · Day28 실습 07

**실행한 모드:** `offline_fixture` (`python 01_basic/07_debug_comparison/main.py --offline`, pytest `2 passed in 0.12s`)

**작성 TODO:** `score_delta`, `find_problem_stage`

## 1. 질문·입력
- 어떤 `question_id`를 사용했는가?
  - `Q01`, `Q07`, `Q06`을 사용했습니다. (`dataset_version`: `d28-eval-v1`)
- Gold Label을 Target 입력에 전달하지 않았는가?
  - 네. `target_inputs(qby[qid])`만 `baseline`과 `rerank_only` 실행에 전달하고, 평가 및 단계 진단(`find_problem_stage`)에서만 `gold[qid]`를 참조했습니다.

## 2. 실제 확인한 출력
- 결과 JSON과 핵심 점수·출처 ID:
  - `Q01`: `baseline_recall=1.0`, `rerank_recall=1.0`, `delta_recall=0.0`, `diagnosis="context_miss"`
  - `Q07`: `baseline_recall=0.5`, `rerank_recall=1.0`, `delta_recall=0.5` (+0.5 개선), `diagnosis="generation_or_ok"`
  - `Q06`: `baseline_recall=null`, `rerank_recall=null`, `delta_recall=null`, `diagnosis="no_answer"`
- No-answer / 실패 / 정상의 차이:
  - `Q06`은 무정답 질문이므로 `score_delta`가 `null`을 반환해 수치 비교에서 제외되며, `find_problem_stage`도 `no_answer`로 분리합니다.

## 3. 해설
- 왜 이 공식 또는 분기 조건이 필요한가?
  - A/B(또는 Before/After) 비교는 동일한 데이터셋 버전과 실행 모드에서 수행해야 유효하며, `후보 -> Reranking -> Context -> 생성` 순서로 병목을 짚어야 실제 성능 저하 원인을 정확히 개선할 수 있습니다.
- 평가 결과가 좋지 않다면 다음에 수정할 모듈은 어디인가?
  - `Q01`처럼 `context_miss`가 발생하면 Reranker 이후 최종 Context에 포함되는 문서 수(Top-N)나 Context 구성 로직을 수정해야 합니다.

## 4. 11월 26일 Agent와 연결
- Agent가 이 RAG 검색 Tool을 사용하기 전에 추가로 확인해야 할 것은 무엇인가?
  - 파이프라인 버전 업그레이드(예: `rerank_only` 적용) 시 기존 질문셋에서 회귀(Regression)가 없는지, 그리고 변경된 Context 구성이 Agent의 Citation/권한 검증과 호환되는지 확인해야 합니다.
