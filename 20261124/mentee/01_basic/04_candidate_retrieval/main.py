"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def make_candidate_request(case):
    """candidate_k와 context_k는 다른 제한값입니다."""
    # candidate_k(후보 검색 개수)는 Reranking을 고려해 context_k(최종 컨텍스트 개수)보다 크게 설정
    return {
        'query': case['question'],
        'category': case['category'],
        'candidate_k': 10,
        'context_k': 3,
    }


def fetch_documents(retriever, payload):
    """Day26에서 배운 Runnable.invoke로 후보 Document를 받아옵니다."""
    # LangChain Runnable 인터페이스의 invoke()로 검색기(Retriever)에 요청 페이로드 전달
    return retriever.invoke(payload)


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 04 · 04_candidate_retrieval')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[4](args.offline,[make_candidate_request,fetch_documents])
    path=save_report(HERE,'day27_04_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 04 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()

"""
[실습 04 전체 요약]
1. 검색 단계의 candidate_k(후보 수)와 LLM에 전달할 context_k(최종 문맥 수)를 분리해 요청 페이로드를 구성합니다.
2. candidate_k를 context_k보다 넉넉히 설정해야 후속 Reranking 단계에서 정답 문서를 상위로 올릴 여지가 생깁니다.
3. LangChain Runnable.invoke()를 통해 검색기에서 후보 Document 리스트를 일관된 방식으로 조회합니다.
"""
