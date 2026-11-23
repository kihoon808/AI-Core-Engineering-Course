"""Day26 실습 7 · 기본필수. 실행 위치와 무관하게 현재 역할 폴더를 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

from coursekit.io import save_json, show_success
from coursekit.data import example_hit
from coursekit.checkpoints import (
    hits_to_documents, build_context, NO_ANSWER, RagServiceError, receive_bundle,
)
from coursekit.fixtures import fixture_bundle
from coursekit.reporting import execution_record


def common_cases():
    """의도적으로 만든 세 입력입니다. 실제 모델의 응답 로그가 아닙니다."""
    answered = {
        "status": "answered",
        "answer": "일반 기준으로 15분까지는 지각입니다. 사전 승인을 받았다면 운영실에 확인합니다.",
        "source_ids": [201], "missing_information": "",
    }
    insufficient = {
        "status": "insufficient_context", "answer": NO_ANSWER,
        "source_ids": [], "missing_information": "정확한 과제 마감 날짜가 자료에 없습니다.",
    }
    unknown = {**answered, "source_ids": [999]}
    return [
        {"name": "normal", "bundle": fixture_bundle(answered)},
        {"name": "insufficient", "bundle": fixture_bundle(insufficient)},
        {"name": "unknown_source", "bundle": fixture_bundle(unknown)},
    ]


def allowed_source_ids(included_docs):
    """입력: 실제 Context에 포함된 Document 목록 / 출력: set[int]."""
    # 실제 Context에 포함된 문서들의 metadata에서만 citation_id를 수집하여 허용 출처 집합을 구성
    return {doc.metadata["citation_id"] for doc in included_docs}


def inspect_case(case, provided_ids):
    """검증 결과를 JSON으로 기록합니다. 원문 의미의 참/거짓은 자동 판정하지 않습니다."""
    # receive_bundle로 수신 상태, 파싱, 자료형 및 허용 출처(provided_ids) 규칙을 순차 검증
    try:
        validated = receive_bundle(case["bundle"], provided_ids)
        return {
            "case": case["name"],
            "outcome": "accepted",
            "error": None,
            "result": validated.model_dump(),
            "human_review_required": True,
        }
    except RagServiceError as exc:
        return {
            "case": case["name"],
            "outcome": "rejected",
            "error": str(exc),
            "result": None,
            "human_review_required": False,
        }


def run():
    documents = hits_to_documents([example_hit()])
    context, included_docs = build_context(documents)
    provided_ids = allowed_source_ids(included_docs)
    cases = common_cases()
    return {
        "source_mode": "validation_fixtures",
        "execution": execution_record("offline"),
        "context": context, "included_ids": sorted(provided_ids),
        "cases": [inspect_case(case, provided_ids) for case in cases],
        "grounding_review": "reports/review.md에서 숫자·조건·예외와 원문 위치를 직접 대조합니다.",
    }


def main():
    report = run()
    path = save_json(HERE, "validation_report.json", report)
    show_success("07 · 고정 입력 검증표 (모델·DB 미실행)", path)
    for row in report["cases"]:
        print(row["case"], row["outcome"], row["error"])
    print("accepted는 기계 검사를 통과했다는 뜻입니다. 원문 대조를 마쳐야 학습이 완료됩니다.")


if __name__ == "__main__":
    main()

"""
[실습 07 핵심 요약]
1. Context에 실제로 포함된 문서(included_docs)에서만 citation_id를 추출해 허용 출처 집합을 제한합니다.
2. receive_bundle을 통해 수신 상태, 파싱, 자료형 및 허용 출처 여부를 순차 검증하고 accepted/rejected로 기록합니다.
3. 자동 검증을 통과(accepted)하더라도 원문이 답변을 실제로 지지하는지(Grounding)는 사람의 별도 검토가 필요합니다.
"""
