"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def plan_queries(base, extras):
    """원 질문을 포함한 서로 다른 질문 2개로 시작합니다."""
    # 원 질문(base)을 첫 번째로 포함하고, extras에서 공백/중복을 제거해 순서를 유지하며 결합
    queries = []
    seen = set()
    for q in [base, *(extras or [])]:
        q_norm = q.strip()
        if q_norm and q_norm not in seen:
            seen.add(q_norm)
            queries.append(q_norm)
    return queries


def merge_candidates(pairs):
    """chunk_id를 중복 제거 키로 사용하고 found_by_query를 Metadata에 기록합니다."""
    # chunk_id를 기준으로 동일 청크를 하나로 통합하되, 어떤 질문에서 검색되었는지 found_by_query에 추적
    merged_by_id = {}
    for query, docs in pairs:
        for doc in docs:
            cid = doc.metadata['chunk_id']
            if cid not in merged_by_id:
                # 원본 Document의 metadata를 복사해 found_by_query 리스트 초기화
                doc.metadata = dict(doc.metadata)
                doc.metadata['found_by_query'] = [query]
                merged_by_id[cid] = doc
            else:
                found = merged_by_id[cid].metadata.setdefault('found_by_query', [])
                if query not in found:
                    found.append(query)
    return list(merged_by_id.values())


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 03 · 03_multi_query')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[3](args.offline,[plan_queries,merge_candidates])
    path=save_report(HERE,'day27_03_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 03 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()

"""
[실습 03 전체 요약]
1. 하나의 원 질문(base)과 확장 질문(extras)을 결합해 중복 없는 다중 검색 질문 리스트를 생성합니다.
2. 각 질문으로 검색된 Document 결과들을 chunk_id 기준으로 중복 제거하여 단일 후보 리스트로 통합합니다.
3. 통합된 각 청크의 metadata['found_by_query']에 해당 청크를 찾아낸 질문들을 기록해 검색 기여도를 추적합니다.
4. 이를 통해 단일 질문 검색의 재현율(Recall) 한계를 보완하고 후속 Reranking 단계로 정제된 후보를 전달합니다.
"""
