"""Day28 실습 06 · 01_basic · 실행 진입점.
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


def safe_target_input(example: dict) -> dict:
    """question_id·question·category·history만 새 dict로 복사하고 Gold·Reference를 제외하세요."""
    # Gold/Reference 정답 정보 누출을 막기 위해 허용된 입력 필드만 화이트리스트 방식으로 복사
    allowed_keys = ("question_id", "question", "category", "history")
    return {key: example.get(key) for key in allowed_keys}

def invoke_target(target, request: dict) -> dict:
    """실제 Runnable.invoke(request)를 호출하고 결과가 dict이며 질문 ID가 같은지 확인하세요."""
    # LangChain Runnable 인터페이스의 invoke() 메서드로 Target 실행
    response = target.invoke(request)
    # 반환 타입이 dict인지 검증
    if not isinstance(response, dict):
        raise TypeError("Target 실행 결과는 dict여야 합니다.")
    # 요청과 응답의 question_id가 일치하는지 검증하여 결과 뒤섞임 방지
    if response.get("question_id") != request.get("question_id"):
        raise ValueError("응답의 question_id가 요청과 일치하지 않습니다.")
    return response


def main():
    parser=argparse.ArgumentParser(description="Day28 RAG Evaluation 실습")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--offline',action='store_true',help='고정 학습 데이터만 실행(기본값)')
    mode.add_argument('--live',action='store_true',help='실제 CUDA GPU/DB/LLM 연결. 06~08만 지원하며 API 비용 발생 가능')
    args=parser.parse_args()
    hooks={
        "safe_target_input":safe_target_input,
        "invoke_target":invoke_target
    }
    # 학생 과제 함수가 실제 서비스가 아니라 이 지도에 정의된 실습 단계에서 호출됩니다.
    try:
        result=execute(6,hooks,live=args.live,level='01_basic')
    except Exception as exc:
        # 실패 기록에는 Key·Password·원본 Prompt를 포함하지 않습니다.
        failure={'status':'execution_failed','exercise':6,
                 'stage':getattr(exc,'stage','evaluation'),
                 'error_type':type(exc).__name__, 'mode':'live' if args.live else 'offline_fixture'}
        write_json(Path(__file__).resolve().parent/'outputs'/'failure.json',failure)
        raise
    output=Path(__file__).resolve().parent/'outputs'/'result.json'
    write_json(output,result)
    # 학생이 코드로 만든 설명 보고서는 별도 Markdown 파일로 저장합니다.
    if isinstance(result.get('markdown_report'),str):
        (output.parent/'report.md').write_text(result['markdown_report'],encoding='utf-8')
    print('Day28 실습 6 · 01_basic ·',result['mode'])
    print('출력:',output)
    return result

if __name__=='__main__':
    main()

"""
[실습 06 요약]
1. safe_target_input(): question_id, question, category, history만 추출해 Gold/Reference 누출을 원천 차단합니다.
2. invoke_target(): LangChain Runnable의 invoke()를 호출하고 dict 반환 여부 및 question_id 일치를 검증합니다.
3. --offline 실행 시 3개 질문에 대한 Target 실행 결과를 outputs/result.json에 기록합니다.
"""
