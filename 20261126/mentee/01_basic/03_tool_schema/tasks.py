"""03 · @tool·Pydantic·JSON Schema · 기본필수.

DB: 기존 report_agent_lab / 반드시 SELECT.
"""
import json


def validate_id(report_id: int) -> int:
    """실제 reports.report_id에 해당하는 1 이상의 정수만 허용한다."""
    if isinstance(report_id, bool) or not isinstance(report_id, int) or report_id < 1:
        raise ValueError("report_id는 1 이상의 정수여야 합니다.")
    return report_id


def register_status_tool():
    """@tool과 Pydantic args_schema로 DB 상태 조회 Tool을 등록해 반환한다."""
    from langchain.tools import tool
    from pydantic import BaseModel, ConfigDict, Field

    class StatusInput(BaseModel):
        # 스키마에 정의되지 않은 임의 필드(task_id 등) 전달을 차단
        model_config = ConfigDict(extra="forbid")
        report_id: int = Field(gt=0, description="기존 reports.report_id; task_id 아님")

    @tool("lookup_status", args_schema=StatusInput)
    def lookup_status(report_id: int) -> str:
        """기존 reports.report_id의 인덱싱 상태(index_status)와 revision을 읽기 전용 조회한다."""
        from coursekit.db import fetch_report_status

        result = fetch_report_status(validate_id(report_id))
        return json.dumps(result, ensure_ascii=False, default=str)

    return lookup_status


"""
[코드 요약]
- validate_id는 bool, 음수, 0, 비정수 입력을 ValueError로 차단하고 1 이상의 report_id만 통과시킨다.
- register_status_tool은 Pydantic extra='forbid' 기반의 StatusInput 스키마를 @tool('lookup_status')에 바인딩한다.
- 실제 호출 시 coursekit.db.fetch_report_status를 지연 임포트해 기존 report_agent_lab에서 읽기 전용 조회를 수행한다.
"""
