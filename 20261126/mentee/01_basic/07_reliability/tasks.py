"""07 · Tool 실패·권한·반복 상한 · 기본필수.

DB: 기존 report_agent_lab / 반드시 SELECT.
"""


def validate_report_id(value) -> int:
    """DB 쿼리 실행 전에 report_id(1 이상 정수) 유효성을 엄격히 검증한다."""
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError("report_id는 양의 정수여야 합니다.")
    if isinstance(value, str):
        # 선행 0이나 부호·공백이 포함된 비정수 문자열을 사전에 차단
        if not value.isdecimal() or value.startswith("0"):
            raise ValueError("report_id 문자열은 선행 0 없는 양의 정수여야 합니다.")
    parsed = int(value)
    if parsed < 1:
        raise ValueError("report_id는 1 이상이어야 합니다.")
    return parsed


def classify_error(exc: Exception) -> dict:
    """예외 유형에 따라 오류 코드를 분류하고 비밀정보·SQL 원문 노출을 차단한다."""
    if isinstance(exc, ValueError):
        return {
            "status": "error",
            "error_code": "INVALID_INPUT",
            "retryable": False,
            "message": "입력 값이 올바르지 않습니다.",
        }
    if isinstance(exc, PermissionError):
        return {
            "status": "error",
            "error_code": "PERMISSION_DENIED",
            "retryable": False,
            "message": "허용되지 않은 접근입니다.",
        }
    if isinstance(exc, (TimeoutError, ConnectionError, OSError)):
        return {
            "status": "error",
            "error_code": "CONNECTION_ERROR",
            "retryable": True,
            "message": "외부 서비스 또는 DB 연결에 실패했습니다.",
        }

    # 알 수 없는 내부 오류도 예외 원문(str(exc))을 그대로 노출하지 않음
    return {
        "status": "error",
        "error_code": "INTERNAL_ERROR",
        "retryable": False,
        "message": "요청 처리 중 내부 오류가 발생했습니다.",
    }


"""
[코드 요약]
- validate_report_id는 DB 조회 전에 bool, 음수, 소수, 선행 0 문자열 등 잘못된 인자를 ValueError로 차단한다.
- classify_error는 입력 오류(INVALID_INPUT), 권한 오류(PERMISSION_DENIED), 연결 오류(CONNECTION_ERROR), 내부 오류를 구분한다.
- 예외 원문(str(exc))을 반환하지 않고 정제된 오류 코드와 메시지만 반환해 비밀번호·SQL 원문 노출을 방지한다.
"""
