"""Day28 실습 02 · 01_basic · 실행 진입점.
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


def select_gold(question_id: str, gold: dict) -> list[str]:
    """gold[question_id]에서 관련 청크 ID 목록을 읽어 중복 없는 list로 반환하세요. 모델 검색 결과를 입력으로 쓰지 마세요."""
    # 평가용 Gold 딕셔너리에서 해당 질문의 정답 청크 ID 목록을 조회 (없으면 빈 리스트)
    raw_ids = gold.get(question_id, [])
    # 입력 순서를 유지하면서 중복 ID를 제거하여 반환
    return list(dict.fromkeys(raw_ids))

def validate_gold_ids(ids: list[str], corpus: dict) -> bool:
    """ID 중복이 없고 모든 ID가 Corpus에 실제 존재하는지 검사하세요."""
    # 1. 리스트 내 중복 ID가 있는지 set 길이 비교로 확인
    if len(ids) != len(set(ids)):
        return False
    # 2. 모든 Gold ID가 실제 corpus 키에 존재하는지 검증 (무정답 빈 리스트도 True)
    return all(chunk_id in corpus for chunk_id in ids)


def main():
    parser=argparse.ArgumentParser(description="Day28 RAG Evaluation 실습")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--offline',action='store_true',help='고정 학습 데이터만 실행(기본값)')
    mode.add_argument('--live',action='store_true',help='실제 CUDA GPU/DB/LLM 연결. 06~08만 지원하며 API 비용 발생 가능')
    args=parser.parse_args()
    hooks={
        "select_gold":select_gold,
        "validate_gold_ids":validate_gold_ids
    }
    # 학생 과제 함수가 실제 서비스가 아니라 이 지도에 정의된 실습 단계에서 호출됩니다.
    try:
        result=execute(2,hooks,live=args.live,level='01_basic')
    except Exception as exc:
        # 실패 기록에는 Key·Password·원본 Prompt를 포함하지 않습니다.
        failure={'status':'execution_failed','exercise':2,
                 'stage':getattr(exc,'stage','evaluation'),
                 'error_type':type(exc).__name__, 'mode':'live' if args.live else 'offline_fixture'}
        write_json(Path(__file__).resolve().parent/'outputs'/'failure.json',failure)
        raise
    output=Path(__file__).resolve().parent/'outputs'/'result.json'
    write_json(output,result)
    # 학생이 코드로 만든 설명 보고서는 별도 Markdown 파일로 저장합니다.
    if isinstance(result.get('markdown_report'),str):
        (output.parent/'report.md').write_text(result['markdown_report'],encoding='utf-8')
    print('Day28 실습 2 · 01_basic ·',result['mode'])
    print('출력:',output)
    return result

if __name__=='__main__':
    main()

"""
[실습 02 요약]
1. select_gold(): gold[question_id]에서 관련 청크 ID를 조회하고 순서를 유지한 채 중복을 제거해 반환합니다.
2. validate_gold_ids(): 반환된 Gold ID 목록에 중복이 없고 모든 ID가 corpus에 실제 존재하는지 검증합니다.
3. --offline 실행 시 Q01, Q05, Q06, Q07의 Gold 어노테이션과 무정답(빈 목록) 케이스를 outputs/result.json에 기록합니다.
"""
