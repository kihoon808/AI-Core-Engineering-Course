# 수행 기록 · Day28 실습 01

**실행한 모드:** `offline_fixture` (`python 01_basic/01_failure_diagnosis/main.py --offline`, pytest `2 passed in 0.09s`)

**작성 TODO:** `classify_case`, `describe_evidence`

## 1. 질문·입력
- 어떤 `question_id`를 사용했는가?
  - 실습 01은 `failure_cases.json`의 실패 진단 케이스 `F01`, `F02`, `F03`, `F04`, `F05`를 입력으로 사용했습니다. (`dataset_version`: `d28-eval-v1`)
- Gold Label을 Target 입력에 전달하지 않았는가?
  - 네. `classify_case`와 `describe_evidence`는 평가용 진단 플래그(`system_error`, `candidate_has_gold`, `context_has_gold`, `answer_grounded`)만 참조하며, 정답 문서 ID(Gold Label)를 Target 실행 입력으로 전달하지 않았습니다.

## 2. 실제 확인한 출력
- 결과 JSON과 핵심 점수·출처 ID:
  - `outputs/result.json` (`exercise=1`, `level=01_basic`, `mode=offline_fixture`, `dataset_version=d28-eval-v1`)
  - `F01`: `retrieval_candidate_miss` (정답 문서가 검색 후보 밖에 있음)
  - `F02`: `retrieval_context_miss` (검색 후보에는 있으나 최종 Context Top-N에서 제외됨)
  - `F03`: `generation_ungrounded` (Context에 근거는 있으나 답변이 근거에 기반하지 않음)
  - `F04`: `system_error` (API 인증 오류 / GPU Out of Memory 등 시스템 장애)
  - `F05`: `ok` (시스템, 검색 후보, Context, 답변 근거 모두 정상)
- No-answer / 실패 / 정상의 차이:
  - 시스템 장애(`system_error`)는 모델/검색 품질 문제가 아닌 인프라·인증 실패이며, 검색 실패(`retrieval_candidate_miss`, `retrieval_context_miss`)와 생성 실패(`generation_ungrounded`), 정상(`ok`)을 단계별로 분리해 진단했습니다.

## 3. 해설
- 왜 이 공식 또는 분기 조건이 필요한가?
  - `System -> Candidate -> Context -> Generation` 순서로 검사해야 앞단 장애(예: 시스템 오류나 후보 누락)를 뒷단(생성 환각) 오류로 오판하지 않고 정확한 원인 위치를 특정할 수 있습니다.
- 평가 결과가 좋지 않다면 다음에 수정할 모듈은 어디인가?
  - `retrieval_candidate_miss`가 많으면 Query Rewrite, 임베딩 모델 또는 1차 Retriever(Top-K)를 개선하고, `retrieval_context_miss`가 많으면 Reranker(Cross-Encoder) 및 Context Top-N 구성을 수정해야 합니다. `generation_ungrounded`가 많으면 프롬프트의 근거 강제 지침이나 LLM 모델을 점검합니다.

## 4. 11월 26일 Agent와 연결
- Agent가 이 RAG 검색 Tool을 사용하기 전에 추가로 확인해야 할 것은 무엇인가?
  - 검색 결과의 출처(Citation)와 문서 접근 권한(RBAC), 그리고 Tool 호출 시 발생할 수 있는 시스템 오류(`system_error`) 및 빈 결과(No-answer) 처리 정책을 사전에 검증해야 합니다.
