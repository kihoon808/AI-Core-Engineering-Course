"""Day22 · 메시지와 출력 계약 | PPT 14~23 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

import json
from coursekit.support import parse_args, guarded, execute_case, emit
from coursekit.request import OUTPUT_FORMAT, build_request as checkpoint_request
from coursekit.response import get, output_text

def make_request(model, instructions, question, selected, *, structured=True):
    # TODO D22-02-B01: 질문과 선택 지식만 user input으로 직렬화하세요.
    # 입력·완료 기준: selected_ids가 아닌 선택된 지식의 id·title·content·category를 보냅니다. expected_behavior는 넣지 않습니다.
    payload = {"question": question, "knowledge": selected} # 전달받은 question과 선택 지식 목록 selected를 직렬화 대상 payload로 구성
    serialized = json.dumps(payload, ensure_ascii=False) # 사용자 입력 문자열 생성

    # TODO D22-02-B02: 공급자용 Schema를 요청의 text.format으로 연결하세요.
    # 입력·완료 기준: response_format이 아니라 Responses의 text.format입니다. Wire와 로컬 KnowledgeAnswer는 다릅니다.
    request = checkpoint_request(model, instructions, question, selected, structured=False)
    request["input"] = [{"role": "user", "content": serialized}]
    # 출력 스키마 계약을 text 필드 아래 {"format": OUTPUT_FORMAT} 형태로 바인딩
    request["text"] = {"format": OUTPUT_FORMAT}
    return request

def response_gate(response):
    # TODO D22-02-B03: 거절 콘텐츠와 미완료 상태를 먼저 구분하세요.
    # 입력·완료 기준: API status와 answer JSON의 status는 다릅니다. 거절을 형식 오류로 바꾸지 않습니다.
    for item in get(response, "output", []) or []:
        if get(item, "type") == "message":
            for part in get(item, "content", []) or []:
                if get(part, "type") == "refusal":
                    return None, "refused"
    if get(response, "status") != "completed":
        return None, get(response, "status") or "response_error"

    # TODO D22-02-B04: 완료 응답에서도 빈 본문을 검사한 뒤 원문을 반환하세요.
    # 입력·완료 기준: 원문을 수정해 유효한 JSON처럼 만들지 않습니다. 로컬 검증기는 다음 단계에서 실행됩니다.
    raw = output_text(response)
    if not raw.strip():
        return None, "empty_output"
    return raw, None

def main():
    args=parse_args(HERE)
    cases=["D02"]
    for case_id in ([args.case] if args.case else cases):
        result=execute_case(args,case_id,request_builder=make_request,hooks={"gate":response_gate})
        emit(args,result)
        if result["run_status"] in {"auth_error","quota_error","permission_error","not_run"}:
            break

if __name__=="__main__":
    guarded(main)
