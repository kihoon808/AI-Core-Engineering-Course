"""Day27 강의 실습. 실행은 역할 폴더에서 Python으로 실행합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
ROLE_ROOT=next(p for p in HERE.parents if (p/'coursekit').is_dir())
sys.path.insert(0,str(ROLE_ROOT))


import argparse

from coursekit.workshops import STAGE_RUNNERS

from coursekit.io import save_report



def diagnose_stage(case):
    """어떤 문제가 먼저 발생했는지 위에서부터 조건을 검사합니다."""
    # 1. 시스템/인덱스 준비 여부와 권한, 최신성 등 선행 조건을 검색 결과보다 먼저 확인
    if not case.get('ready', True):
        return 'Index / System Not Ready'
    if not case.get('authorized', True):
        return 'Permission / Authorization'
    if not case.get('current', True):
        return 'Freshness / Version'
    # 2. 사용자 질문 자체가 모호하면 검색 이전에 Query Rewrite가 필요함
    if case.get('ambiguous'):
        return 'Query Ambiguity'
    # 3. 후보군(Candidates)에 정답 문서가 없으면 Candidate Retrieval 단계 실패
    if not case.get('gold_in_candidates'):
        return 'Candidate Retrieval'
    # 4. 후보군에는 있으나 최종 Context에 포함되지 못했으면 Reranking/순위 실패
    if not case.get('gold_in_context'):
        return 'Reranking / Context'
    # 5. Context는 적절하나 출처(source_ids) 검증에 실패한 경우
    if case.get('valid_source') is False:
        return 'Source Verification'
    return 'Pass'


def recommend_action(stage):
    """문제 단계에 맞는 개선 방법을 반환합니다. Reranker는 누락된 후보를 새로 찾지 않습니다."""
    # 진단된 실패 단계별로 대응되는 파이프라인 개선 전략을 매핑
    actions = {
        'Index / System Not Ready': '인덱스 및 시스템 준비 상태 확인',
        'Permission / Authorization': '사용자 권한 및 문서 접근 제어(RBAC) 정책 확인',
        'Freshness / Version': '문서 최신 버전 동기화 및 인덱스 갱신 확인',
        'Query Ambiguity': 'Query Rewrite 적용 또는 사용자에게 질문 구체화 요청',
        'Candidate Retrieval': 'Candidate Retrieval 개선 (Hybrid Search, Candidate K 확대 등; Reranker는 누락된 후보를 새로 찾지 않음)',
        'Reranking / Context': 'Reranking 후보 순위 및 Context 포함 기준 확인',
        'Source Verification': 'source_ids 구조 검증 및 답변 Grounding 검증 강화',
        'Pass': '정상 통과 (추가 조치 불필요)',
    }
    return actions.get(stage, f'알 수 없는 단계: {stage}')


def main():
    parser=argparse.ArgumentParser(description='Day27 실습 01 · 01_failure_diagnosis')
    parser.add_argument('--offline',action='store_true',help='교육용 고정 데이터·점수. 모델 품질 실측이 아닙니다.')
    args=parser.parse_args()
    # Day27: 일부 진단 실습 외에는 기본 실행이 실제 모델·DB·LLM 경로입니다.
    report=STAGE_RUNNERS[1](args.offline,[diagnose_stage,recommend_action])
    path=save_report(HERE,'day27_01_'+('fixture' if args.offline else 'live')+'.json',report)
    print('실습 01 결과:', path)
    print('보고서를 확인하고 reports/review.md에 원문 대조·실행 모드를 기록하세요.')

if __name__=='__main__':main()

"""
[실습 01 전체 요약]
1. RAG 파이프라인의 실패 원인을 선행 조건(권한, 최신성) -> 질문 모호성 -> 후보 누락 -> 순위/컨텍스트 -> 출처 검증 순으로 진단합니다.
2. 권한 오류(F06)나 최신성 오류(F07)를 후보 누락(F02)보다 먼저 검사해야 원인이 올바르게 분리됩니다.
3. Reranker는 기존 후보군의 순위만 재조정할 뿐 누락된 후보를 새로 찾지 못하므로, 후보 누락 시 Retrieval 단계를 개선해야 합니다.
4. 진단 결과와 개선 방안을 JSON 리포트로 저장하여 각 단계별 실패 지점을 명확히 파악합니다.
"""
