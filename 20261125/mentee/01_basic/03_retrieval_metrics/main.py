"""Day28 실습 03 · 01_basic · 실행 진입점.
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


def calculate_recall(ranked: list[str], gold: list[str], k: int) -> float | None:
    """Top-k에서 찾은 Gold 개수 / 전체 Gold 개수를 계산하세요. Gold가 빈 질문은 None을 반환하세요."""
    # Gold가 비어 있는 무정답(No-answer) 질문은 Recall 평균에서 제외하기 위해 None 반환
    if not gold:
        return None
    # Top-k 내 고유 Gold 적중 개수를 전체 고유 Gold 개수로 나누어 Recall@k 계산
    hits = count_gold_hits(ranked, gold, k)
    return hits / len(set(gold))

def count_gold_hits(ranked: list[str], gold: list[str], k: int) -> int:
    """Top-k 목록과 Gold의 교집합 크기를 반환하세요. 중복 ID는 한 번만 셉니다."""
    # Top-k 슬라이싱 후 set 교집합(&)으로 중복 없이 적중 개수 계산
    return len(set(ranked[:k]) & set(gold))


def main():
    parser=argparse.ArgumentParser(description="Day28 RAG Evaluation 실습")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--offline',action='store_true',help='고정 학습 데이터만 실행(기본값)')
    mode.add_argument('--live',action='store_true',help='실제 CUDA GPU/DB/LLM 연결. 06~08만 지원하며 API 비용 발생 가능')
    args=parser.parse_args()
    hooks={
        "calculate_recall":calculate_recall,
        "count_gold_hits":count_gold_hits
    }
    # 학생 과제 함수가 실제 서비스가 아니라 이 지도에 정의된 실습 단계에서 호출됩니다.
    try:
        result=execute(3,hooks,live=args.live,level='01_basic')
    except Exception as exc:
        # 실패 기록에는 Key·Password·원본 Prompt를 포함하지 않습니다.
        failure={'status':'execution_failed','exercise':3,
                 'stage':getattr(exc,'stage','evaluation'),
                 'error_type':type(exc).__name__, 'mode':'live' if args.live else 'offline_fixture'}
        write_json(Path(__file__).resolve().parent/'outputs'/'failure.json',failure)
        raise
    output=Path(__file__).resolve().parent/'outputs'/'result.json'
    write_json(output,result)
    # 학생이 코드로 만든 설명 보고서는 별도 Markdown 파일로 저장합니다.
    if isinstance(result.get('markdown_report'),str):
        (output.parent/'report.md').write_text(result['markdown_report'],encoding='utf-8')
    print('Day28 실습 3 · 01_basic ·',result['mode'])
    print('출력:',output)
    return result

if __name__=='__main__':
    main()

"""
[실습 03 요약]
1. count_gold_hits(): Top-k 검색 결과와 Gold 집합의 교집합 크기를 중복 없이 계산합니다.
2. calculate_recall(): 적중 개수를 전체 고유 Gold 개수로 나누어 Recall@k를 구하며, 무정답(빈 Gold) 질문은 None을 반환합니다.
3. --offline 실행 시 Q01, Q07, Q06의 Recall@3 및 적중 수를 outputs/result.json에 기록합니다.
"""
