"""Day21 실습 03: 작업 분해와 정보 부족. 실행: python main.py"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import DATA, read_json, write_json, write_text, run

# 기준: Day21 PPT 21~27장. 실제 모델 호출/실습 데이터 수정은 하지 않습니다.
# outputs는 실행 시 생성됩니다. 05/08의 모델 응답은 직접 수집한 원문만 등록합니다.

def analyze_card(card):
    # TODO D21-03-B01: 질문이 요구하는 사실과, 제공 자료가 지원하는 사실을 구분하세요.

    # 질문이 요구하는 필수 사실 목록 추출
    required = list(card["required"])

    # 제공된 지식 컨텍스트가 지원하는 사실 맵
    supported = card["supported"]

    # 요구 사실 중 제공 지식에서 뒷받침되지 않는 결손 사실 식별
    missing = [fact for fact in required if fact not in supported]

    # 모순되거나 상충하는 정보 목록
    conflicts = list(card["conflicts"])

    # TODO D21-03-B02: 하나라도 근거가 부족하면 수업의 정보 부족 상태를 선택하세요.
    # 결손 사실이나 모순이 하나라도 존재하면 insufficient_context로 결정 (부분 답변/추측 금지)
    status = "insufficient_context" if missing or conflicts else "answered"
    source_ids = []
    if status == "answered":
        # 완전한 근거가 확보된 경우에만 관련 지식 ID 집계
        for fact in required:
            source_ids.extend(supported[fact])
    # ID 중복 제거 및 입력 순서 유지
    source_ids = list(dict.fromkeys(source_ids))
    result = {
        "case_id": card["case_id"],
        "required": required,
        "supported_facts": list(supported),
        "missing": missing,
        "conflicts": conflicts,
        "status": status,
        "source_ids": source_ids,
        "basis": "teacher_authored_fact_card",
    }
    return result

def main():
    cards=read_json(DATA/"decomposition_cards.json")
    # TODO D21-03-B03: 정상·정보 부족의 판단과 최종 출력 지시를 저장하세요.

    # 기본 실습 대상인 C01(정상), C02(정보 부족) 카드 분석
    results = [analyze_card(c) for c in cards[:2]]

    # 사실 대조·결손 정보 처리·최종 JSON 출력 요구 지시문 작성
    instruction = "질문이 요구하는 사실과 근거를 대조하세요. 부족하면 추측하지 말고 필요한 정보를 적으세요. 내부 사고 기록 대신 최종 JSON만 반환하세요."

    # C01은 answered, C02는 insufficient_context 상태 불변조건 확인
    assert results[0]["status"] == "answered" and results[1]["status"] == "insufficient_context"
    write_json(HERE / "outputs" / "task_cards.json", results)
    write_text(HERE / "outputs" / "task_instruction.txt", instruction)
    print("[03] 판단 카드 완료. 근거 대조는 사람의 판단이 포함됩니다.")

if __name__ == "__main__":
    run(main)
