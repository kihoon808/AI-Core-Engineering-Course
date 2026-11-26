# Day29 · 03 · @tool·Pydantic·JSON Schema · 기본필수 리뷰

## 1. 구현 내역 (`tasks.py`)
- `validate_id(report_id: int) -> int`:
  - `bool`, 음수, 0, 비정수 입력을 `ValueError`로 차단하고 1 이상의 `report_id`만 허용합니다.
- `register_status_tool()`:
  - `ConfigDict(extra="forbid")`와 `Field(gt=0)`가 적용된 `StatusInput` Pydantic 모델을 `@tool("lookup_status", args_schema=StatusInput)`에 연결해 등록된 Tool 객체를 반환합니다.

## 2. 검증 결과
- 구조 점검 (`python 01_basic/03_tool_schema/main.py --check`):
  - `TODO 함수: ['register_status_tool', 'validate_id']` 정상 출력 확인
- 오프라인 계약 테스트 (`pytest tests/test_contracts.py -k "test_01_basic_" -v`):
  - `01_basic` 01에서 08까지 8개 전체 통과 (`8 passed in 0.21s`)
- 실제 실행 (`python 01_basic/03_tool_schema/main.py`):
  - `.backendenv`에 `langchain>=1.3.14,<2` 설치 후 재실행하여 입력 검사, JSON Schema 생성 및 실제 DB 호출(`fetch_report_status`) 진입 확인 (`DATABASE_URL` 미설정으로 DB 연결 단계에서 중단).

## 3. 학습 기록 (요약)
1. `@tool`과 Pydantic `args_schema`를 결합하면 LLM이 생성할 인자 스펙을 JSON Schema로 명확히 노출하고, `extra="forbid"`로 존재하지 않는 필드(`task_id` 등) 유입을 차단할 수 있습니다.
2. Python 타입 힌트(`report_id: int`)만으로는 `bool`이나 음수 입력을 막을 수 없으므로 `Field(gt=0)` 및 런타임 검증(`validate_id`)을 병행해야 합니다.
3. Tool 함수의 docstring과 필드 `description`은 모델이 어떤 상황에서 어떤 인자를 채워 호출할지 결정하는 핵심 메타데이터로 동작합니다.
