"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def apply_rewrite(question, history, offline):
    """offline이면 고정 예시, 기본 실행이면 실제 ChatPromptTemplate → Chat Model을 호출합니다."""
    # coursekit.rewrite.rewrite_query를 호출해 대화 History 기반 질문 재작성 수행
    # offline=True면 고정 Fixture를, False면 실제 ChatPromptTemplate + Structured Output LLM 체인을 실행
    from coursekit.rewrite import rewrite_query
    return rewrite_query(question, history, offline=offline)


def record_rewrite(original, result):
    """원래 질문을 검색 질문으로 덮어쓰지 않습니다."""
    # 원 질문(original_question)과 검색용 질문(search_query)을 분리해 보존
    # 모호한 질문은 status='clarification_required'로 기록해 검색 진행을 차단
    return {
        'original_question': original,
        'status': result.status,
        'search_query': result.search_query,
        'reason': result.reason,
    }


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 02 · 02_query_rewrite')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[2](args.offline,[apply_rewrite,record_rewrite])
    path=save_report(HERE,'day27_02_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 02 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()

"""
[실습 02 전체 요약]
1. 대화 History에서 생략된 대상을 복원해 독립적인 검색 질문(search_query)으로 재작성합니다.
2. offline 모드에서는 고정 Fixture를, live 모드에서는 ChatPromptTemplate과 Structured Output LLM 체인을 사용합니다.
3. 대상을 특정할 수 없는 모호한 질문은 억지로 추측하지 않고 status='clarification_required'로 확인을 요청합니다.
4. original_question과 search_query를 분리 기록하여 원래 사용자 질문이 훼손되지 않도록 보존합니다.
"""
