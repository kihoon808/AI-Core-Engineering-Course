"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record

def format_hit(hit: dict) -> str:
    """Hit 한 건의 ID·위치·본문을 한 문자열 블록으로 반환합니다."""
    # [인용 ID] 출처 위치 헤더 아래에 본문을 붙여 단일 근거 블록 구성
    return f"[{hit['citation_id']}] {hit['source_locator']}\n{hit['body']}"

def make_context(hits: list[dict], max_items: int = 2) -> tuple[str, list[int]]:
    """앞에서 최대 max_items건을 골라 Context와 같은 선택의 ID 목록을 반환합니다."""
    # 상위 max_items건만 선택해 빈 줄(\n\n)로 연결한 Context와 실제 포함된 ID 목록을 함께 반환
    selected = hits[:max_items]
    blocks = [format_hit(h) for h in selected]
    included_ids = [h["citation_id"] for h in selected]
    return "\n\n".join(blocks), included_ids

def main():
    hit = example_hit()
    context, included_ids = make_context([hit])
    report = {
        "execution": execution_record("local_python"),
        "context": context,
        "included_ids": included_ids,
        "input_source": "lecture_fixture",
        "character_count": len(context),
    }
    path = save_json(HERE, "hit_context.json", report)
    show_success("02 기본필수", path)

if __name__ == "__main__":
    main()

"""
[실습 02 요약: Hit에서 Context 만들기]
1. format_hit은 검색 결과(Hit) 한 건을 `[citation_id] source_locator`와 본문이 이어진 문자열 블록으로 변환합니다.
2. make_context는 최대 max_items건의 Hit만 잘라 빈 줄(\n\n)로 연결하고, 실제로 Context에 포함된 citation_id 목록을 함께 반환합니다.
3. 빈 입력일 때는 빈 문자열과 빈 목록을 반환해 가짜 근거를 채우지 않으며, 원본 hits 리스트는 변경하지 않습니다.
"""
