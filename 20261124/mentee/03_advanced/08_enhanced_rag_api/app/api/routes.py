"""단계별 역할 분리: app/api/routes.py / 독립 실행은 main.py. """

def check_http_response(response):
    """성공 응답의 source_ids와 실제 연결된 sources의 ID가 같은지 검사합니다."""
    # BEGIN D27-08-A03
    if response.status_code != 200:
        return {'status_code': response.status_code, 'source_ids_match': False, 'checked': False}
    body = response.json()
    source_ids = set(body.get('source_ids', []))
    attached_ids = {s.get('chunk_id') for s in body.get('sources', []) if isinstance(s, dict)}
    return {
        'status_code': response.status_code,
        'source_ids_match': source_ids == attached_ids,
        'source_ids': sorted(source_ids),
        'attached_ids': sorted(attached_ids),
        'checked': True,
    }
    # END D27-08-A03
