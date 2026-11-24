"""단계별 역할 분리: schemas/request.py / 독립 실행은 main.py. """

def prepare_pipeline_request(case):
    """원 질문과 History를 함께 보존하고 검색용 질문은 Chain 내부에서 만듭니다."""
    # RagRequest 스키마에 맞춰 원 질문(query), 대화 이력(history), 카테고리(category)를 전달
    return {
        'query': case['question'],
        'history': case.get('history', []),
        'category': case['category'],
    }
