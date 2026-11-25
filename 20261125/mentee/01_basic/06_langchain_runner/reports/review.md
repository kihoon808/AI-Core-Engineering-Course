# 수행 기록 · Day28 실습 06

**실행한 모드:** `offline_fixture` (`python 01_basic/06_langchain_runner/main.py --offline`, pytest `1 passed, 1 skipped in 0.04s`)

**작성 TODO:** `safe_target_input`, `invoke_target`

## 1. 질문·입력
- 어떤 `question_id`를 사용했는가?
  - `execute(6, ...)`는 `questions[:3]`(`Q01`, `Q02`, `Q03`)을 입력으로 사용합니다.
- Gold Label을 Target 입력에 전달하지 않았는가?
  - 네. `safe_target_input`에서 `question_id`, `question`, `category`, `history` 4개 키만 화이트리스트 방식으로 복사하여 Gold/Reference 누출을 차단했습니다.

## 2. 실제 확인한 출력
- 결과 JSON과 핵심 점수·출처 ID:
  - 현재 실행 환경(시스템 Python)에 `langchain_core` 패키지가 설치되어 있지 않아 `as_runnable` 단계에서 `ModuleNotFoundError: No module named 'langchain_core'`가 발생했습니다.
  - `pytest`는 `1 passed, 1 skipped in 0.04s`로 종료되었습니다.
- No-answer / 실패 / 정상의 차이:
  - `invoke_target`에서 반환 타입(`dict`)과 `question_id` 일치를 검증하므로, 비정상 응답이나 ID 불일치 시 즉시 예외를 발생시켜 잘못된 평가 집계를 막습니다.

## 3. 해설
- 왜 이 공식 또는 분기 조건이 필요한가?
  - 평가 대상(Target)에 Gold나 Reference가 들어가면 데이터 누출이 발생해 공정한 평가가 불가능하므로 입력 필터링(`safe_target_input`)이 필수입니다. 또한 LangChain `Runnable.invoke()` 규약을 통해 오프라인 Fixture와 라이브(`--live`) 실행을 동일한 인터페이스로 교체할 수 있습니다.
- 평가 결과가 좋지 않다면 다음에 수정할 모듈은 어디인가?
  - `langchain_core` 등 필수 패키지가 설치된 가상환경(`.venv`)을 구성한 뒤, Target 파이프라인(Retriever/Reranker/Prompt)을 점검해야 합니다.

## 4. 11월 26일 Agent와 연결
- Agent가 이 RAG 검색 Tool을 사용하기 전에 추가로 확인해야 할 것은 무엇인가?
  - Tool 입력 스키마에 민감 정보나 정답 힌트가 섞이지 않는지, 그리고 `Runnable.invoke()` 호출 실패(타임아웃, 네트워크 오류, 스키마 불일치) 시 Agent가 안전하게 예외를 처리하는지 확인해야 합니다.
