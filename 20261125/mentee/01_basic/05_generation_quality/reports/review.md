# 수행 기록 · Day28 실습 05

**실행한 모드:** `offline_fixture` (`python 01_basic/05_generation_quality/main.py --offline`, pytest `2 passed in 0.15s`)

**작성 TODO:** `claim_faithfulness`, `describe_claim_result`

## 1. 질문·입력
- 어떤 `question_id`를 사용했는가?
  - `generation_claims.json`의 생성 품질 검수 케이스 `G01`, `G02`, `G03`, `G04`를 사용했습니다. (`dataset_version`: `d28-eval-v1`)
- Gold Label을 Target 입력에 전달하지 않았는가?
  - 네. `claim_faithfulness`와 `describe_claim_result`는 사람 검수 레이블(`human_fixture`)의 `claims` 목록만 받아 Faithfulness를 계산하며, Target 생성 입력으로 Gold를 전달하지 않습니다.

## 2. 실제 확인한 출력
- 결과 JSON과 핵심 점수·출처 ID:
  - `G01`: `faithfulness=0.6666666666666666` (2/3), `reason="비지원 Claim: 벌금이 5만원"`
  - `G02`: `faithfulness=0.0` (0/1), `reason="비지원 Claim: 내일 오후 6시 마감"`
  - `G03`: `faithfulness=1.0`, `reason="모든 Claim 지원"`
  - `G04`: `faithfulness=null`, `reason="Claim 없음"`
- No-answer / 실패 / 정상의 차이:
  - `G04`는 추출된 Claim이 없는 경우이므로 `faithfulness=null`과 `"Claim 없음"`으로 분리하여, 모든 Claim이 지원되는 정상(`G03`, `1.0`)이나 근거 없는 환각(`G02`, `0.0`)과 구분했습니다.

## 3. 해설
- 왜 이 공식 또는 분기 조건이 필요한가?
  - Faithfulness는 Reference Answer와의 일치 여부가 아니라, **검색된 Context가 답변 내 각 Claim을 실제로 지지하는지**를 측정합니다. 비지원 Claim을 구체적으로 기록해야 어떤 문장이 환각인지 추적할 수 있습니다.
- 평가 결과가 좋지 않다면 다음에 수정할 모듈은 어디인가?
  - Faithfulness가 낮다면 생성 프롬프트(Context 외 추론 금지 지침 강화) 또는 LLM 모델/디코딩 설정(temperature 하향)을 수정해야 합니다.

## 4. 11월 26일 Agent와 연결
- Agent가 이 RAG 검색 Tool을 사용하기 전에 추가로 확인해야 할 것은 무엇인가?
  - 모델이 반환한 Citation ID가 실제 검색 Context에 존재하는지, 그리고 근거가 불충분할 때 Agent가 환각 답변을 생성하지 않고 추가 검색이나 사용자 확인을 요청하도록 가드레일이 동작하는지 확인해야 합니다.
