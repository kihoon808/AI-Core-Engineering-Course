"""단계별 역할 분리: app/services/rag_service.py / 독립 실행은 main.py. """

def wire_fastapi(chain):
    """API 요청의 role 문자열을 신뢰하지 않고 서버에서 learner 역할을 지정합니다."""
    # BEGIN D27-08-A02
    from coursekit.api import create_app
    return create_app(chain, trusted_role='learner')
    # END D27-08-A02
