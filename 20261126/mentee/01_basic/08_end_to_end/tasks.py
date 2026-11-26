"""08 · FastAPI -> Agent -> Tool -> 응답 · 기본필수.

DB: 기존 report_agent_lab / 반드시 SELECT.
"""


def default_question() -> str:
    """보고서 내용 검색과 63번 보고서 인덱싱 상태를 함께 묻는 기본 질문을 반환한다."""
    return (
        "RAG 근거 인용 정확도 향상과 관련된 보고서 내용을 설명하고, "
        "보고서 63번의 인덱싱 상태도 알려줘."
    )


def api_response(run: dict) -> dict:
    """Agent 실행 결과를 API 응답 계약(상태·답변·출처 검증·인증 범위)으로 변환한다."""
    if not isinstance(run, dict):
        raise ValueError("Agent 실행 결과는 dict여야 합니다.")

    status = str(run.get("status") or "error")
    citation_ids_valid = bool(run.get("citation_ids_valid", False))
    verified_evidence_ids = list(run.get("verified_evidence_ids") or [])
    tool_trace = list(run.get("tool_trace") or [])

    # 출처 ID 검증 실패 시 API 응답 상태를 실패로 명확히 전환
    if status == "completed" and not citation_ids_valid:
        status = "citation_validation_failed"

    return {
        "status": status,
        "answer": str(run.get("answer") or ""),
        "citation_ids_valid": citation_ids_valid,
        "verified_evidence_ids": verified_evidence_ids,
        "tool_trace": tool_trace,
        # 로컬 실습 전용 API이므로 사용자 인증·소유권 ACL은 미구현 상태임을 명시
        "auth_scope": "local_only_no_user_auth",
    }


"""
[코드 요약]
- default_question은 문서 검색과 보고서 63번 인덱싱 상태 조회를 동시에 요구하는 표준 질의를 반환한다.
- api_response는 Agent 실행 결과에서 status, answer, citation_ids_valid, verified_evidence_ids, tool_trace를 분리해 반환한다.
- 출처 ID 검증이 실패하면 status를 citation_validation_failed로 전환하고 로컬 전용 무인증(local_only_no_user_auth) 범위를 명시한다.
"""
