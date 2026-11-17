# Day22 첫 실제 응답 | PPT 6~13 | 01_basic

from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded, execute_case, emit
from coursekit.io import write_json

def make_first_request(model, instructions, question, selected, *, structured=False):
    # TODO D22-01-B01: 첫 요청의 model·instructions·input·출력 상한·store를 완성하세요.
    # 입력·완료 기준: 입력은 전달받은 값입니다. 새 질문·임의 모델을 하드코딩하지 않으며 JSON Schema는 다음 교시입니다.

    #전달 받은 값들을 바탕으로 API 규격에 맞춘 요청 파라미터들을 구성
    request = {"model": model, "instructions": instructions, "input": question,
               "reasoning": {"effort": "none"}, "max_output_tokens": 1200,
               "store": False, "service_tier": "default"}
    return request

def create_response(client, request, stream=False):
    # TODO D22-01-B02: Responses API를 한 번 호출하고 반환값을 돌려주세요.
    # 입력·완료 기준: 키를 직접 문자열로 쓰지 않습니다. 한 함수 호출은 create 한 번만 수행합니다.

    #전달받은 클라이언트를 통해 1회 호출 및 응답 객체 반환
    response = client.responses.create(**request, stream=stream)
    return response

def make_view(result):
    # TODO D22-01-B03: 키 없이 source·model·종료 상태·응답 ID를 요약하세요.
    # 입력·완료 기준: 미실행이면 response_id는 None입니다. 0이나 가짜 응답 ID를 채우지 않습니다.

    #API 키 등 민감정보를 제외하고 메타데이터만을 추출하여 요약 딕셔너리 생성
    last = result.get("attempts", [])[-1] if result.get("attempts") else {}
    summary = {
        "source_mode": result["source_mode"],
        "model": result.get("model"),
        "run_status": result["run_status"],
        "response_id": last.get("response_id")
    }
    return summary

def main():
    args=parse_args(HERE)
    result=execute_case(args,"FIRST",request_builder=make_first_request,hooks={"create":create_response})
    emit(args,result)
    view=make_view(result)
    write_json(args.output_dir/"connection_view.json",view)

if __name__=="__main__":
    guarded(main)
