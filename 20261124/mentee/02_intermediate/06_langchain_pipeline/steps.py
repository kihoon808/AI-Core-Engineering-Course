"""단계별 역할 분리: steps.py / 독립 실행은 main.py. """

def prepare_pipeline_request(case):
    """원 질문과 History를 함께 보존하고 검색용 질문은 Chain 내부에서 만듭니다."""
    # RagRequest 스키마에 맞춰 원 질문(query), 대화 이력(history), 카테고리(category)를 전달
    return {
        'query': case['question'],
        'history': case.get('history', []),
        'category': case['category'],
    }


def wire_langchain_pipeline(dependencies, offline):
    """LCEL는 Runnable을 준비할 뿐이고 .invoke()가 실행 시작점입니다."""
    # coursekit.pipeline.create_rag_pipeline으로 Rewrite -> Retrieval -> Rerank -> Generate LCEL 체인 조립
    from coursekit.pipeline import create_rag_pipeline
    return create_rag_pipeline(*dependencies, offline=offline)