"""05 · PostgreSQL Read-only lookup_status · 기본필수.

DB: 기존 report_agent_lab / 반드시 SELECT.
"""


def parse_report_id(value) -> int:
    """reports.report_id로 사용할 양의 정수를 엄격하게 검증해 반환한다."""
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError("report_id는 양의 정수여야 합니다.")
    if isinstance(value, str):
        # 선행 0이나 부호/공백이 섞인 비정수 문자열을 차단
        if not value.isdecimal() or value.startswith("0"):
            raise ValueError("report_id 문자열은 선행 0 없는 양의 정수여야 합니다.")
    parsed = int(value)
    if parsed < 1:
        raise ValueError("report_id는 1 이상이어야 합니다.")
    return parsed


def status_view(raw: dict) -> dict:
    """DB 인덱싱 상태(index_status)와 벡터 정합성(vector_fresh)을 구분해 반환한다."""
    if not isinstance(raw, dict):
        raise ValueError("raw 상태 데이터는 dict여야 합니다.")

    index_status = raw.get("index_status")
    vector_fresh = bool(raw.get("vector_fresh", False))

    # index_status가 ready여도 vector_fresh가 False면 실제 RAG 검색 사용 불가
    return {
        "status": raw.get("status", "unknown"),
        "report_id": raw.get("report_id"),
        "revision": raw.get("revision"),
        "index_status": index_status,
        "vector_fresh": vector_fresh,
        "ready_for_rag": index_status == "ready" and vector_fresh,
    }


"""
[코드 요약]
- parse_report_id는 bool, 소수, 음수, 선행 0 문자열을 차단하고 1 이상의 정수 report_id만 반환한다.
- status_view는 DB의 index_status(pending/ready/failed)와 실제 벡터 최신성(vector_fresh)을 분리해 표시한다.
- 두 값이 모두 충족될 때만 ready_for_rag를 True로 판정해 상태 오판을 방지한다.
"""
