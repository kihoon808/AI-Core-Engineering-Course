"""04 · 기존 RAG를 rag_search Tool로 · 기본필수.

DB: 기존 report_agent_lab / 반드시 SELECT.
"""

_ALLOWED_CATEGORIES = frozenset({
    "ALL",
    "EXPERIMENT",
    "DAILY_WORK",
    "RESEARCH_PLAN",
    "DATA_PROCESSING",
    "PROMPT",
    "MEETING",
})


def prepare_search(query: str, category: str = "ALL") -> dict:
    """검색어와 허용된 6개 카테고리(+ALL)를 검증해 정규화된 요청 dict를 반환한다."""
    if not isinstance(query, str) or not query.strip() or len(query.strip()) > 500:
        raise ValueError("검색어는 1에서 500자 사이의 문자열이어야 합니다.")
    if not isinstance(category, str):
        raise ValueError("category는 문자열이어야 합니다.")

    # 대소문자·공백을 정규화한 뒤 허용된 카테고리 집합과 대조
    normalized_category = category.strip().upper()
    if normalized_category not in _ALLOWED_CATEGORIES:
        raise ValueError(f"허용되지 않는 category입니다: {category}")

    return {
        "query": query.strip(),
        "category": normalized_category,
    }


def invoke_rag(request: dict) -> dict:
    """검증된 요청으로 실제 기존 DB(pgvector) 및 CUDA E5/Reranker RAG를 호출한다."""
    if not isinstance(request, dict):
        raise ValueError("request는 dict여야 합니다.")

    # 실행 직전에도 입력 계약을 재검증하여 잘못된 파라미터 전달을 차단
    validated = prepare_search(
        request.get("query", ""),
        request.get("category", "ALL"),
    )

    # 오프라인 단위 테스트 시 coursekit 의존성을 피하기 위해 호출 시점에 지연 임포트
    from coursekit.rag import rag_answer

    return rag_answer(validated["query"], validated["category"])


"""
[코드 요약]
- prepare_search는 검색어(1~500자)와 6개 허용 카테고리(+ALL)를 검증해 정규화된 요청 딕셔너리를 생성한다.
- invoke_rag는 요청을 재검증한 뒤 coursekit.rag.rag_answer를 호출해 기존 pgvector DB와 CUDA E5·Reranker 기반 RAG를 실행한다.
- 가짜 검색 결과를 생성하지 않고 실제 DB 조회 및 LLM 근거 응답 계약을 그대로 연결한다.
"""
