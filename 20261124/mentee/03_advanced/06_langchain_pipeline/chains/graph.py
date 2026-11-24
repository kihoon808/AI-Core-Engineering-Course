"""단계별 역할 분리: chains/graph.py / 독립 실행은 main.py. """

def wire_langchain_pipeline(dependencies, offline):
    """LCEL는 Runnable을 준비할 뿐이고 .invoke()가 실행 시작점입니다."""
    # coursekit.pipeline.create_rag_pipeline으로 Rewrite -> Retrieval -> Rerank -> Generate LCEL 체인 조립
    from coursekit.pipeline import create_rag_pipeline
    return create_rag_pipeline(*dependencies, offline=offline)
