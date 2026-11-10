"""조회 계산만 분리합니다. HTTP 응답이나 파일 저장은 여기서 처리하지 않습니다."""
def select_category(entries: list[dict], category: str | None) -> list[dict]:
    if category is None:
        return entries
    # BEGIN A06-01
    # TODO A06-01: category가 있는 경우 정확히 일치하는 항목들의 목록을 반환하세요. 이 함수에서 파일을 읽거나 HTTPException을 사용하지 마세요.
    # HTTP/스토리지 종속성 없는 순수 계산 로직으로 카테고리 일치 항목 필터링
    return [entry for entry in entries if entry["category"] == category]
    # END A06-01


def find_entry(entries: list[dict], knowledge_id: int) -> dict | None:
    # BEGIN A06-02
    # TODO A06-02: entries에서 ID가 같은 항목을 찾아 반환하세요. 없으면 아래 return None으로 진행하세요.
    # 식별자가 일치하는 첫 번째 엔트리 탐색 후 반환
    for entry in entries:
        if entry["id"] == knowledge_id:
            return entry
    # END A06-02
    return None

"""
[핵심 개념 요약]
1. 비즈니스 로직 분리(Pure Functions): I/O나 프레임워크 종속성 없는 순수 계산 함수로 분리하여 단위 테스트 용이성을 극대화합니다.
2. 예외 처리의 호출자 위임: 조회 함수는 단순히 None을 반환하고, 404 HTTP 예외 발생 여부는 상위 라우터(main.py)가 결정합니다.
3. 데이터 파이프라인 단순화: 원본 메모리 리스트를 받아 필터링된 새 리스트나 엔터티를 반환하는 단순 선형 탐색을 구현합니다.
"""

