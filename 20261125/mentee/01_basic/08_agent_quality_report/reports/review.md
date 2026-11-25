# 수행 기록 · Day28 실습 08

**실행한 모드:** `offline_fixture` (`python 01_basic/08_agent_quality_report/main.py --offline`, pytest `2 passed in 0.17s`)

**작성 TODO:** `evaluate_one`, `summarize_all`

## 1. 질문·입력
- 어떤 `question_id`를 사용했는가?
  - 전체 8개 질문(`Q01` - `Q08`)을 사용했습니다. (`dataset_version`: `d28-eval-v1`)
- Gold Label을 Target 입력에 전달하지 않았는가?
  - 네. `target_inputs(example)`만 `target_fixture`에 전달해 `run` 결과를 생성한 뒤, `evaluate_one`에서만 `gold[qid]`와 `grades[qid]`를 결합해 평가했습니다.

## 2. 실제 확인한 출력
- 결과 JSON과 핵심 점수·출처 ID:
  - `summary`: `total_questions=8`, `no_answer_count=1`, `error_count=0`, `with_citations_count=0`, `mean_recall_at_3=1.0`
  - `Q01`: `recall_at_k=1.0`, `precision_at_k=0.3333333333333333`, `rr_at_k=1.0`, `ndcg_at_k=1.0`, `included_ids=["FAC-102-C1", "FAC-101-C1"]`
- No-answer / 실패 / 정상의 차이:
  - 무정답 질문(1건)은 `no_answer_count`로 별도 집계하고 `mean_valid`를 통해 평균 Recall 계산에서 제외하여 지표 왜곡을 방지했습니다.

## 3. 해설
- 왜 이 공식 또는 분기 조건이 필요한가?
  - Trace 필드(`ranked_ids`, `included_ids`)가 누락되었을 때 빈 리스트로 조용히 대체하면 시스템/로깅 오류가 0점 성능으로 둔갑하므로 즉시 예외를 발생시켜야 합니다. 또한 No-answer 질문을 평균에서 분리해야 실제 검색 품질을 정확히 파악할 수 있습니다.
- 평가 결과가 좋지 않다면 다음에 수정할 모듈은 어디인가?
  - `error_count > 0`이면 Target 실행 파이프라인 및 로깅/인프라를 먼저 복구하고, `mean_recall_at_3`이 낮다면 Retriever/Reranker를 개선합니다.

## 4. 11월 26일 Agent와 연결
- Agent가 이 RAG 검색 Tool을 사용하기 전에 추가로 확인해야 할 것은 무엇인가?
  - 전체 평가 요약 리포트의 품질 게이트(Recall, 오류 건수, Citation 포함 여부)를 통과했는지, 그리고 문서 접근 권한(RBAC) 및 최신성 검증이 함께 동작하는지 확인해야 합니다.
