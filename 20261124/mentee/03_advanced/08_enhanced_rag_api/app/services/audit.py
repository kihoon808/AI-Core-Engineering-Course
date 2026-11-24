"""단계별 역할 분리: app/services/audit.py / 독립 실행은 main.py. """

def audit_http_response(payload, response):
    """HTTP 오류를 정보 부족 응답으로 숨기지 않고 Stage·모드·상태를 기록합니다."""
    # BEGIN D27-08-A04
    body = response.json()
    detail = body.get('detail') if isinstance(body, dict) else None
    stage = detail.get('stage') if isinstance(detail, dict) else None
    error_code = detail.get('code') if isinstance(detail, dict) else None
    return {
        'http_status': response.status_code,
        'is_error': response.status_code >= 400,
        'stage': stage,
        'error_code': error_code,
        'detail': detail,
        'query': payload.get('query') if isinstance(payload, dict) else None,
        'category': payload.get('category') if isinstance(payload, dict) else None,
    }
    # END D27-08-A04
