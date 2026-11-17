"""Day22 · 명시적 모델 선택 | PPT 53~59 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded
from coursekit.config import choose_model as checkpoint_choose
from coursekit.labs import routing_lab

def route(mode, models):
    # TODO D22-07-B01: fast·quality만허용하고실제모델과선택이유를반환하세요.
    # 입력·완료 기준: 알수없는모드를fast로조용히바꾸지않습니다. quality권한없으면not_run입니다.
    # 허용 모드(fast, quality) 검증 및 명시적 모델 선택 반환 (임의 자동 대체 금지)
    if mode not in {"fast", "quality"}:
        raise ValueError("지원하지 않는 실행 모드")
    return checkpoint_choose(mode, models)

def record_view(result):
    # TODO D22-07-B02: 어떤모델이든동일한결과필드로비교하세요.
    # 입력·완료 기준: 고가모델이항상더좋다는결론을미리넣지않습니다.
    # 모델 간 공정한 비교를 위해 결과에서 필요한 공통 메트릭 필드만 추출
    fields = [
        "case_id", "source_mode", "model", "route_reason", "run_status",
        "answer_object", "evidence_ok", "usage", "request_ms", "estimated_usd"
    ]
    return {key: result.get(key) for key in fields}

def comparison_modes():
    # TODO D22-07-B03: 명시적비교에서만fast·quality를한번씩선택하세요.
    # 입력·완료 기준: 기본run은한모델만호출합니다. compare는계정권한·예산확인후선택합니다.
    # 명시적 비교 시 fast와 quality 모드를 각각 1회씩 실행 대상으로 지정
    return ["fast", "quality"]

def main():
    args=parse_args(HERE)
    routing_lab(args,router=route,record_view=record_view,compare_modes=comparison_modes)

if __name__=="__main__":
    guarded(main)
