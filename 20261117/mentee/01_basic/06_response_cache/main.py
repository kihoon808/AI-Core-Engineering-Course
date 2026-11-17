"""Day22 · 승인 응답 캐시 | PPT 47~52 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from copy import deepcopy
from coursekit.support import parse_args, guarded, cache_lab
from coursekit.io import write_json, digest
from coursekit.request import build_request as checkpoint_request
from coursekit.cache import read_cache as checkpoint_cache

def key_of(request, scope, validator_version="day21-v1"):
    # TODO D22-06-B01: 질문뿐 아니라 모델·전체요청·Schema·검증버전·scope로 캐시키를 만드세요.
    # 입력·완료 기준: API키는포함하지않습니다. 전체본문이키에들어가야같은ID의내용변경도감지합니다.
    # API 키를 제외한 모델, 전체 요청, 포맷, 검증버전, scope 기반으로 SHA-256 캐시 키 생성
    basis = {
        "scope": scope,
        "model": request["model"],
        "request": request,
        "format": request.get("text", {}).get("format"),
        "validator_version": validator_version,
    }
    return digest(basis)

def approved_cache(cache, key, now, provided_ids, *, expected_source, scope):
    # TODO D22-06-B02: 현재문맥·실행출처·scope와함께 제공된 안전한캐시검사를 호출하세요.
    # 입력·완료 기준: 만료·미승인·현재출처불일치는미스입니다. 승인하려면tools/review.py로사람이기록합니다.
    # 만료, 승인 여부, 출처 모드 일치 여부를 검증하는 안전 캐시 조회 호출
    return checkpoint_cache(
        cache,
        key,
        now,
        provided_ids,
        expected_source=expected_source,
        scope=scope,
    )

def compare_context_keys():
    # TODO D22-06-B03: 같은 ID의 본문 변경이 캐시키를 바꾸는지 확인하세요.
    # 입력·완료 기준: 이 키 비교는 전송0회의 모의검사입니다. 실제 재사용은 먼저 생성· 사람 승인 후 reuse 명령으로 확인합니다.
    from coursekit.io import input_parts
    from coursekit.config import load_settings
    case, selected, instructions = input_parts("H01")
    model = load_settings("simulated").models["fast"]
    first = checkpoint_request(model, instructions, case["question"], selected)
    changed = deepcopy(selected)  # 원본 JSON 수정을 방지하기 위한 복사본

    # 동일 ID라도 컨텍스트 내용이 변경되면 캐시 키가 달라짐을 검증 (Cache Miss)
    changed[0]["content"] += " 실행 환경도 함께 적습니다."
    second = checkpoint_request(model, instructions, case["question"], changed)
    assert key_of(first, "classroom-demo") != key_of(second, "classroom-demo")
    return {"changed_context_miss": True, "source_mode": "simulated", "new_api_send_count": 0}

def main():
    args=parse_args(HERE)
    write_json(args.output_dir/"cache_key_checks.json",compare_context_keys())
    result=cache_lab(args,key_builder=key_of,cache_reader=approved_cache)

if __name__=="__main__":
    guarded(main)
