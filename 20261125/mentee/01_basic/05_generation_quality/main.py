"""Day28 실습 05 · 01_basic · 실행 진입점.
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


def claim_faithfulness(claims: list[dict]) -> float | None:
    """Claim 목록에서 근거가 지지하는 Claim 비율을 계산하세요. Claim이 없으면 None."""
    # Claim 목록이 비어 있으면 Faithfulness를 계산할 수 없으므로 None 반환
    if not claims:
        return None
    # supported가 True인 Claim 개수를 전체 Claim 개수로 나누어 비율 계산
    supported_count = sum(1 for claim in claims if claim.get("supported"))
    return supported_count / len(claims)

def describe_claim_result(claims: list[dict]) -> str:
    """비지원 Claim을 이름과 함께 기록하세요. “모든 Claim 지원”과 “Claim 없음”은 구별합니다."""
    # Claim이 아예 없는 경우와 모든 Claim이 지원되는 경우를 명확히 구분
    if not claims:
        return "Claim 없음"
    # 근거가 지지하지 않는(supported=False) Claim의 텍스트 목록 추출
    unsupported = [claim.get("text", "(이름 없음)") for claim in claims if not claim.get("supported")]
    if not unsupported:
        return "모든 Claim 지원"
    return f"비지원 Claim: {', '.join(unsupported)}"


def main():
    parser=argparse.ArgumentParser(description="Day28 RAG Evaluation 실습")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--offline',action='store_true',help='고정 학습 데이터만 실행(기본값)')
    mode.add_argument('--live',action='store_true',help='실제 CUDA GPU/DB/LLM 연결. 06~08만 지원하며 API 비용 발생 가능')
    args=parser.parse_args()
    hooks={
        "claim_faithfulness":claim_faithfulness,
        "describe_claim_result":describe_claim_result
    }
    # 학생 과제 함수가 실제 서비스가 아니라 이 지도에 정의된 실습 단계에서 호출됩니다.
    try:
        result=execute(5,hooks,live=args.live,level='01_basic')
    except Exception as exc:
        # 실패 기록에는 Key·Password·원본 Prompt를 포함하지 않습니다.
        failure={'status':'execution_failed','exercise':5,
                 'stage':getattr(exc,'stage','evaluation'),
                 'error_type':type(exc).__name__, 'mode':'live' if args.live else 'offline_fixture'}
        write_json(Path(__file__).resolve().parent/'outputs'/'failure.json',failure)
        raise
    output=Path(__file__).resolve().parent/'outputs'/'result.json'
    write_json(output,result)
    # 학생이 코드로 만든 설명 보고서는 별도 Markdown 파일로 저장합니다.
    if isinstance(result.get('markdown_report'),str):
        (output.parent/'report.md').write_text(result['markdown_report'],encoding='utf-8')
    print('Day28 실습 5 · 01_basic ·',result['mode'])
    print('출력:',output)
    return result

if __name__=='__main__':
    main()

"""
[실습 05 요약]
1. claim_faithfulness(): 답변에서 추출된 Claim 목록 중 근거가 지지하는(supported=True) 비율을 계산하며, Claim이 없으면 None을 반환합니다.
2. describe_claim_result(): 'Claim 없음', '모든 Claim 지원', 그리고 비지원 Claim 목록을 구분해 기록합니다.
3. --offline 실행 시 generation_claims.json 기반 Faithfulness 검수 결과를 outputs/result.json에 저장합니다.
"""
