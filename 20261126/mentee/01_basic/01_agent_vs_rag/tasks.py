"""01 · AI Agent vs 고정 RAG/Workflow · 기본필수.

DB: 기존 report_agent_lab / 반드시 SELECT.
"""

# 문서 본문 검색(RAG) 성격과 DB 상태 조회(lookup_status) 성격을 구분하기 위한 키워드 집합
_RAG_KEYWORDS = ("보고서", "근거", "내용", "설명", "찾아", "검색", "요약", "규정", "rag")
_DB_KEYWORDS = ("인덱싱", "상태", "index_status", "revision", "vector_fresh", "번", "db")


def classify_request(question: str) -> str:
    """질문 성격을 'rag', 'db', 'agent' 중 하나로 분류한다."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("질문은 빈 문자열이 아니어야 합니다.")

    normalized = question.strip().lower()
    has_rag = any(kw in normalized for kw in _RAG_KEYWORDS)
    has_db = any(kw in normalized for kw in _DB_KEYWORDS)

    # 문서 검색과 DB 상태 조회가 모두 필요한 복합 질의는 agent로 분기
    if has_rag and has_db:
        return "agent"
    if has_db:
        return "db"
    # 명시적 DB 상태 키워드가 없는 일반 질의는 기본 문서 검색(rag)으로 처리
    return "rag"


def plan_for_request(question: str) -> dict:
    """분류된 전략에 따라 실행할 Tool 목록 계획을 반환한다."""
    strategy = classify_request(question)

    # 전략별 허용 Tool 매핑 (실제 Agent 루프 실행 전 단계의 계획 수립)
    tool_map = {
        "rag": ["rag_search"],
        "db": ["lookup_status"],
        "agent": ["rag_search", "lookup_status"],
    }
    return {
        "strategy": strategy,
        "tools": tool_map[strategy],
    }


"""
[코드 요약]
- _RAG_KEYWORDS와 _DB_KEYWORDS를 기준으로 사용자 질문을 'rag', 'db', 'agent' 세 가지 처리 성격으로 분류한다.
- 단일 성격 질의는 각각 고정 RAG('rag_search') 또는 DB 상태 조회('lookup_status')로 매핑하고, 복합 질의는 'agent' 전략으로 분기한다.
- plan_for_request는 조건문 기반의 Tool 선택 계획(strategy, tools)을 반환하며, 실제 LLM의 자율 판단 및 ToolMessage 루프와는 구분된다.
"""

