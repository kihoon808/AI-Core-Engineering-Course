"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def create_pairs(question, docs):
    """CrossEncoder 입력은 [질문, 문서본문]의 쌍 목록입니다."""
    # Cross-Encoder는 질문과 문서 본문을 하나의 쌍으로 묶어 직접 상호작용(Attention) 점수를 계산
    return [[question, doc.page_content] for doc in docs]


def rank_documents(question, docs, scorer):
    """Reranker는 후보를 새로 찾지 않고 동일 후보를 순위 변경합니다."""
    if not docs:
        return []
    # [질문, 문서본문] 쌍에 대한 관련도 점수를 계산해 metadata에 기록 후 내림차순 정렬
    pairs = create_pairs(question, docs)
    scores = scorer(pairs)
    ranked = []
    for doc, score in zip(docs, scores):
        doc.metadata = dict(doc.metadata)
        doc.metadata['rerank_score'] = float(score)
        ranked.append(doc)
    ranked.sort(key=lambda d: d.metadata['rerank_score'], reverse=True)
    return ranked


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 05 · 05_cross_encoder_reranking')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[5](args.offline,[create_pairs,rank_documents])
    path=save_report(HERE,'day27_05_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 05 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()

"""
[실습 05 전체 요약]
1. 검색된 후보 문서들을 [질문, 문서본문] 쌍으로 변환해 Cross-Encoder 입력을 구성합니다.
2. scorer가 산출한 rerank_score를 각 Document의 metadata에 저장하고 점수 내림차순으로 재정렬합니다.
3. Reranker는 기존 후보 집합(before_ids)의 순위만 바꿀 뿐 누락된 문서를 새로 검색하지 않습니다.
"""
