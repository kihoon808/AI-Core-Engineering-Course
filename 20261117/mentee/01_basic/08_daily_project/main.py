"""Day22 · AI 지식 답변 생성기 v2 | PPT 60~68 | 01_basic
공통 제공 코드는 교시 독립 시작점입니다. 본 파일의 TODO 함수를 실행 경로에 연결합니다.
"""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.support import parse_args, guarded, daily_project
from coursekit.metrics import summarize_runs
from coursekit.records import table_rows

def project_cases():
    # TODO D22-08-B01: 최종연동확인질문H01·H02·H03을같은순서로지정하세요.
    # 입력·완료 기준: 이미본질문이므로새holdout의일반화성능이라고부르지않습니다.
    # 최종 연동 검증용 질문 H01, H02, H03을 순서대로 지정 (H01은 스트리밍 방식)
    return ["H01", "H02", "H03"]

def project_rows(runs):
    # TODO D22-08-B02: 각실행의상태·사용량·시간을표행으로연결하세요.
    # 입력·완료 기준: 실패한행도버리지않습니다. 모든질문의예상답을실측답으로채우지않습니다.
    # 각 실행의 상태, 사용량, 소요 시간을 테이블 행(Row)으로 변환 (실패 행도 보존)
    return table_rows(runs)

def project_summary(runs):
    # TODO D22-08-B03: 실제·모의·캐시·미실행을분리하여요약하세요.
    # 입력·완료 기준: 소수관찰로P95·SLA·보편적모델우열을주장하지않습니다.
    # 실제, 모의, 캐시, 미실행 결과를 분리하여 통계 요약
    return summarize_runs(runs)

def check_project(runs):
    # TODO D22-08-B04: 자동검사후사람미평가None을유지하고전송상한을확인하세요.
    # 입력·완료 기준: 사람평가는tools/review.py의별도파일로남깁니다. 새API·DB·RAG는만들지않습니다.
    # 사람 검토 전 evidence_ok의 None 상태 유지 및 전송 횟수 상한(4회 이하) 검증
    for run in runs:
        assert run.get("evidence_ok") is None
        assert run.get("new_api_send_count", 0) <= 4
    return True

def main():
    args=parse_args(HERE)
    runs=daily_project(args,prepare_cases=project_cases,make_table=project_rows,finish_summary=project_summary)
    if isinstance(runs,list):
        check_project(runs)

if __name__=="__main__":
    guarded(main)
