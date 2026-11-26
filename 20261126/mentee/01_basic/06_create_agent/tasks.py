"""06 · create_agent + 실제 Tool 2개 · 기본필수.

DB: 기존 report_agent_lab / 반드시 SELECT.
"""


def question_for_agent(report_id: int) -> str:
    """내용 검색과 특정 report_id의 인덱싱 상태를 함께 묻는 복합 질문을 생성한다."""
    if isinstance(report_id, bool) or not isinstance(report_id, int) or report_id < 1:
        raise ValueError("report_id는 1 이상의 정수여야 합니다.")

    # RAG 검색(rag_search)과 DB 상태 조회(lookup_status)를 모두 유도하는 복합 질의 구성
    return (
        f"RAG 근거 인용 정확도 향상과 관련된 보고서 내용을 설명하고, "
        f"보고서 {report_id}번의 인덱싱 상태도 알려줘."
    )


def make_agent():
    """create_agent 기반의 LangChain Agent(Tool 2개, LLM, Tool Call 상한 포함)를 반환한다."""
    # 오프라인 단위 테스트 시 coursekit/LLM 설정 의존을 피하기 위해 호출 시점에 지연 임포트
    from coursekit.agent import build_agent

    return build_agent()


"""
[코드 요약]
- question_for_agent는 report_id(1 이상 정수)를 검증한 뒤 문서 검색과 DB 상태 조회를 동시에 요구하는 복합 질문을 생성한다.
- make_agent는 coursekit.agent.build_agent를 호출해 rag_search·lookup_status Tool 2개와 ToolCallLimitMiddleware가 적용된 Agent를 반환한다.
- 실제 실행 시 LLM이 자율적으로 두 Tool을 선택해 호출하고 ToolMessage 결과를 종합해 답변한다.
"""
