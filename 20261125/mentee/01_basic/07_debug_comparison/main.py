"""Day28 실습 07 · 01_basic · 실행 진입점.
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


def score_delta(before: float | None, after: float | None) -> float | None:
    """같은 질문의 Before/After 점수 변화량을 계산하세요. No-answer(None)는 수치 차이를 만들지 않습니다."""
    # No-answer(None)가 포함된 경우 비교 불가하므로 None 반환
    if before is None or after is None:
        return None
    # 개선 전후 점수 차이(after - before) 계산
    return after - before

def find_problem_stage(run: dict, gold: list[str]) -> str:
    """검색 후보 누락·Reranking 누락·Context 누락·생성 실패 중 어디인지 반환하세요."""
    # 무정답(No-answer) 질문은 실패 단계 진단 대상에서 제외
    if not gold:
        return "no_answer"
    gold_set = set(gold)
    # 1. 1차 검색 후보(candidate_ids)에 Gold가 없으면 검색 후보 누락
    candidates = set(run.get("candidate_ids") or run.get("ranked_ids", []))
    if not (candidates & gold_set):
        return "retrieval_candidate_miss"
    # 2. Reranking 상위 결과(ranked_ids[:3])에 Gold가 없으면 Reranking 누락
    reranked = set(run.get("ranked_ids", [])[:3])
    if not (reranked & gold_set):
        return "reranking_miss"
    # 3. 최종 Context(included_ids)에 Gold가 없으면 Context 누락
    included = set(run.get("included_ids", run.get("ranked_ids", [])[:3]))
    if not (included & gold_set):
        return "context_miss"
    # 4. 앞선 검색/Context 단계가 모두 정상이면 생성 단계 문제로 분류
    return "generation_or_ok"


def main():
    parser=argparse.ArgumentParser(description="Day28 RAG Evaluation 실습")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument('--offline',action='store_true',help='고정 학습 데이터만 실행(기본값)')
    mode.add_argument('--live',action='store_true',help='실제 CUDA GPU/DB/LLM 연결. 06~08만 지원하며 API 비용 발생 가능')
    args=parser.parse_args()
    hooks={
        "score_delta":score_delta,
        "find_problem_stage":find_problem_stage
    }
    # 학생 과제 함수가 실제 서비스가 아니라 이 지도에 정의된 실습 단계에서 호출됩니다.
    try:
        result=execute(7,hooks,live=args.live,level='01_basic')
    except Exception as exc:
        # 실패 기록에는 Key·Password·원본 Prompt를 포함하지 않습니다.
        failure={'status':'execution_failed','exercise':7,
                 'stage':getattr(exc,'stage','evaluation'),
                 'error_type':type(exc).__name__, 'mode':'live' if args.live else 'offline_fixture'}
        write_json(Path(__file__).resolve().parent/'outputs'/'failure.json',failure)
        raise
    output=Path(__file__).resolve().parent/'outputs'/'result.json'
    write_json(output,result)
    # 학생이 코드로 만든 설명 보고서는 별도 Markdown 파일로 저장합니다.
    if isinstance(result.get('markdown_report'),str):
        (output.parent/'report.md').write_text(result['markdown_report'],encoding='utf-8')
    print('Day28 실습 7 · 01_basic ·',result['mode'])
    print('출력:',output)
    return result

if __name__=='__main__':
    main()

"""
[실습 07 요약]
1. score_delta(): 동일 질문의 Before/After 점수 차이(after - before)를 계산하며, No-answer(None)는 None으로 유지합니다.
2. find_problem_stage(): 검색 후보 -> Reranking Top-3 -> 최종 Context 순으로 Gold 포함 여부를 점검해 병목 단계를 진단합니다.
3. --offline 실행 시 baseline과 rerank_only 비교 결과를 outputs/result.json에 기록합니다.
"""
