"""단계별 역할 분리: services/trace.py / 독립 실행은 main.py. """

def validate_trace(result):
    """원 질문·검색용 질문·후보·Context ID를 각각 확인합니다."""
    # trace에 원 질문, 검색 질문, 후보 ID, 최종 Context ID가 모두 기록되었는지 검증
    trace = result.get('trace', {})
    return {
        'has_original_question': bool(trace.get('original_question')),
        'has_search_query': bool(trace.get('search_query')),
        'candidate_count': len(trace.get('candidate_ids', [])),
        'included_count': len(trace.get('included_ids', [])),
        'included_subset_of_candidates': set(trace.get('included_ids', [])).issubset(
            set(trace.get('candidate_ids', []))
        ),
    }
