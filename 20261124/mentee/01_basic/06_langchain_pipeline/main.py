"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))
import argparse
from coursekit.workshops import STAGE_RUNNERS
from coursekit.io import save_report


def prepare_pipeline_request(case):
    """원 질문과 History를 함께 보존하고 검색용 질문은 Chain 내부에서 만듭니다."""
    # RagRequest 스키마에 맞춰 원 질문(query), 대화 이력(history), 카테고리(category)를 전달
    return {
        'query': case['question'],
        'history': case.get('history', []),
        'category': case['category'],
    }


def wire_langchain_pipeline(dependencies, offline):
    """LCEL는 Runnable을 준비할 뿐이고 .invoke()가 실행 시작점입니다."""
    # coursekit.pipeline.create_rag_pipeline으로 Rewrite -> Retrieval -> Rerank -> Generate LCEL 체인을 조립
    from coursekit.pipeline import create_rag_pipeline
    return create_rag_pipeline(*dependencies, offline=offline)


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 06 · 06_langchain_pipeline')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[6](args.offline,[prepare_pipeline_request,wire_langchain_pipeline])
    path=save_report(HERE,'day27_06_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 06 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()

"""
[실습 06 전체 요약]
1. 원 질문과 대화 History, 카테고리, 권한 정보를 포함한 파이프라인 입력 페이로드를 구성합니다.
2. create_rag_pipeline()에 의존성(rewrite, search, rerank, generate)을 주입해 LCEL Runnable 체인을 조립합니다.
3. 체인 조립 시점에는 실행되지 않으며, run_06 내부에서 .invoke(req)를 호출할 때 전체 RAG 흐름이 실행됩니다.
4. 실행 결과에는 최종 응답과 출처(sources), 그리고 원 질문이 보존된 trace가 함께 기록됩니다.
"""
