"""02 · AIMessage.tool_calls / ToolMessage · 기본필수.

DB: 기존 report_agent_lab / 반드시 SELECT.
"""

_ALLOWED_TOOLS = frozenset({"rag_search", "lookup_status"})


def make_request(tool_name: str, args: dict, call_id: str) -> dict:
    """AIMessage.tool_calls의 요청 항목 구조를 생성한다. 실제 도구를 실행하지는 않는다."""
    if tool_name not in _ALLOWED_TOOLS:
        raise ValueError(f"허용되지 않는 Tool 이름입니다: {tool_name}")
    if not isinstance(args, dict):
        raise ValueError("Tool 인수는 dict여야 합니다.")
    if not isinstance(call_id, str) or not call_id.strip():
        raise ValueError("call_id는 비어 있지 않은 문자열이어야 합니다.")

    # 모델이 생성하는 Tool Call 요청 스펙(name, args, id)만 조립
    return {
        "name": tool_name,
        "args": dict(args),
        "id": call_id.strip(),
    }


def match_result(call: dict, result: dict) -> dict:
    """실제 도구 실행 결과를 요청의 tool_call_id와 연결한 ToolMessage 구조로 반환한다."""
    if not isinstance(call, dict) or not call.get("id"):
        raise ValueError("유효한 Tool Call 요청(id 포함)이 필요합니다.")
    if not isinstance(result, dict):
        raise ValueError("Tool 실행 결과는 dict여야 합니다.")

    # 요청 id를 tool_call_id로 매핑하여 LLM 컨텍스트에 전달할 결과 메시지 생성
    return {
        "type": "ToolMessage",
        "tool_call_id": call["id"],
        "name": call.get("name", ""),
        "content": result,
    }


"""
[코드 요약]
- make_request는 허용된 Tool 이름, dict 인수, 호출 ID를 검증해 AIMessage.tool_calls 항목 형식의 요청 딕셔너리를 생성한다.
- match_result는 실제 DB/도구 실행 결과(dict)를 요청의 id(tool_call_id)와 연결해 ToolMessage 형식의 응답 딕셔너리로 묶는다.
- 모델의 도구 호출 요청 단계와 Python 백엔드의 실제 도구 실행·응답 단계를 구조적으로 분리한다.
"""

