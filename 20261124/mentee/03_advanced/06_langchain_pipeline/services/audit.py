"""단계별 역할 분리: services/audit.py / 독립 실행은 main.py. """

def audit_pipeline(result):
    """Stage 시간과 출처 연결을 기록하되 진위 판단은 별도로 수행합니다."""
    # 단계별 소요 시간(timing_ms)과 응답의 source_ids가 실제 sources의 citation_id에 연결되는지 기록
    trace = result.get('trace', {})
    timing_ms = trace.get('timing_ms', {})
    cited_ids = set(result.get('result', {}).get('source_ids', []))
    source_citation_ids = {s.get('citation_id') for s in result.get('sources', [])}
    return {
        'timing_ms': timing_ms,
        'total_ms': round(sum(timing_ms.values()), 3) if timing_ms else 0.0,
        'source_ids_linked': cited_ids.issubset(source_citation_ids),
        'grounding_verified': False,  # 구조 연결만 확인하며 내용 진위 판단은 별도 수행
    }
