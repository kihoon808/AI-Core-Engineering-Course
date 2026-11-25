"""Day28 실습 01 · 01_basic · 실행 진입점.
수강생은 TODO의 요구사항을 해결하고 예상 출력과 비교합니다.
강사용 코드에는 데이터 계약, 단계별 처리 의도와 예외를 주석으로 설명합니다.
"""
from pathlib import Path
import argparse
import sys

ROLE_ROOT = Path(__file__).resolve().parents[2]
if str(ROLE_ROOT) not in sys.path:
    sys.path.insert(0,str(ROLE_ROOT))

from coursekit.eval_workshops import execute
from coursekit.eval_report import write_json


def classify_case(case: dict) -> str:
    """case의 system_error·candidate_has_gold·context_has_gold·answer_grounded를 차례로 확인하고 stage 문자열을 반환하세요. 시스템 장애와 검색 실패를 구분하세요."""
    # 1. 시스템 장애 여부를 최우선으로 확인 (인증 오류, OOM 등 파이프라인 자체 실패)
    if case.get("system_error"):
        return "system_error"
    # 2. 검색 후보(Candidate) 단계에서 정답 문서가 누락되었는지 확인
    if not case.get("candidate_has_gold"):
        return "retrieval_candidate_miss"
    # 3. 후보는 찾았으나 최종 Context(Top-N) 선별/리랭킹 단계에서 제외되었는지 확인
    if not case.get("context_has_gold"):
        return "retrieval_context_miss"
    # 4. Context에 근거가 있음에도 생성된 답변이 근거에 기반하지 않았는지(환각) 확인
    if not case.get("answer_grounded"):
        return "generation_ungrounded"
    # 5. 모든 단계가 정상 통과한 경우
    return "ok"

def describe_evidence(case: dict, stage: str) -> str:
    """분류된 stage를 설명할 수 있는 구체적인 한 줄의 근거를 반환하세요. 빈 문자열은 안 됩니다."""
    # stage별 실패 위치와 원인(후보 누락 vs Context 누락 등)을 구분하는 기본 설명 매핑
    descriptions = {
        "system_error": "시스템 장애(API/GPU 오류 등)로 인해 검색 및 생성 파이프라인이 정상 실행되지 않았습니다.",
        "retrieval_candidate_miss": "정답 문서가 검색 후보(Candidate)에 포함되지 않아 검색 단계에서 누락되었습니다.",
        "retrieval_context_miss": "정답 문서가 검색 후보에는 포함되었으나 최종 Context(Top-N)에서 제외되었습니다.",
        "generation_ungrounded": "Context에 정답 근거가 존재하지만 생성된 답변이 해당 근거에 기반하지 않았습니다.",
        "ok": "시스템, 검색 후보, 최종 Context 및 답변 근거가 모두 정상적으로 검증되었습니다.",
    }
    base = descriptions.get(stage, f"분류 단계({stage})에 대한 근거가 확인되었습니다.")
    # 케이스에 추가 메모(note)가 있으면 근거 문장 뒤에 병기
    note = case.get("note")
    return f"{base} ({note})" if note else base


def main():
    parser=argparse.ArgumentParser(description="Day28 RAG Evaluation 실습")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--offline',action='store_true',help='고정 학습 데이터만 실행(기본값)')
    mode.add_argument('--live',action='store_true',help='실제 CUDA GPU/DB/LLM 연결. 06~08만 지원하며 API 비용 발생 가능')
    args=parser.parse_args()
    hooks={
        "classify_case":classify_case,
        "describe_evidence":describe_evidence
    }
    # 학생 과제 함수가 실제 서비스가 아니라 이 지도에 정의된 실습 단계에서 호출됩니다.
    try:
        result=execute(1,hooks,live=args.live,level='01_basic')
    except Exception as exc:
        # 실패 기록에는 Key·Password·원본 Prompt를 포함하지 않습니다.
        failure={'status':'execution_failed','exercise':1,
                 'stage':getattr(exc,'stage','evaluation'),
                 'error_type':type(exc).__name__, 'mode':'live' if args.live else 'offline_fixture'}
        write_json(Path(__file__).resolve().parent/'outputs'/'failure.json',failure)
        raise
    output=Path(__file__).resolve().parent/'outputs'/'result.json'
    write_json(output,result)
    # 학생이 코드로 만든 설명 보고서는 별도 Markdown 파일로 저장합니다.
    if isinstance(result.get('markdown_report'),str):
        (output.parent/'report.md').write_text(result['markdown_report'],encoding='utf-8')
    print('Day28 실습 1 · 01_basic ·',result['mode'])
    print('출력:',output)
    return result

if __name__=='__main__':
    main()

"""
[실습 01 요약]
1. classify_case(): 시스템 장애 -> 검색 후보 누락 -> Context(Top-N) 누락 -> 생성 근거 미기반 순으로 실패 단계를 분류합니다.
2. describe_evidence(): 분류된 stage에 맞춰 후보 누락과 Context 누락을 구분하는 한 줄 근거를 생성하고 케이스 메모를 병기합니다.
3. --offline 모드로 실행 시 고정 데이터셋(d28-eval-v1) 기반 진단 결과를 outputs/result.json에 저장하며, 테스트 통과를 확인했습니다.
"""
