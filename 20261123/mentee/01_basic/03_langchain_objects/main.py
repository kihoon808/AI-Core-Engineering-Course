"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record

COMPONENT_INPUTS = {
    "Document": "page_content와 metadata를 담아 생성",
    "Retriever": "query·category·candidate_k가 있는 dict",
    "Prompt": "question·context가 있는 dict",
    "Chat Model": "ChatPromptValue 또는 메시지 목록",
}

# 네 가지 핵심 LangChain 구성요소(Document, Retriever, Prompt, Chat Model)의 반환 자료형 매핑
def component_outputs() -> dict[str, str]:
    """강의에서 다룬 네 구성요소의 출력 자료형을 대응시킵니다."""
    return {
        "Document": "Document (page_content, metadata)",
        "Retriever": "list[Document]",
        "Prompt": "ChatPromptValue",
        "Chat Model": "AIMessage",
    }

# 단순 데이터 접근(data)과 실행 인터페이스(invoke) 호출 대상 구분
def access_kinds() -> dict[str, str]:
    """데이터를 읽는 경우와 invoke로 작업을 실행하는 경우를 구분합니다."""
    return {
        "Document": "data",
        "Retriever": "invoke",
        "Prompt": "invoke",
        "Chat Model": "invoke",
    }

# 구성요소별 입출력·접근 방식을 하나의 리포트로 묶어 JSON 파일로 저장
def main():
    outputs = component_outputs()
    access = access_kinds()
    report = {
        "execution": execution_record("concept_review"),
        "components": [{"component": name, "input": value,
                        "output": outputs[name], "access": access[name]}
                       for name, value in COMPONENT_INPUTS.items()],
        "observation": "입력·출력 대응표; Prompt·모델 invoke는 실행하지 않음",
    }
    path = save_json(HERE, "object_contracts.json", report)
    show_success("03 기본필수", path)

if __name__ == "__main__":
    main()

"""
[실습 03 요약]
- LangChain의 네 핵심 구성요소(Document, Retriever, Prompt, Chat Model)가 각각 무엇을 입력받아 어떤 타입을 반환하는지 정리했습니다.
- Document는 본문과 메타데이터를 보관하는 단순 데이터(data)로, Retriever·Prompt·Chat Model은 invoke로 실행하는 구성요소로 구분했습니다.
- 실제 API나 모델 호출 없이 입출력 계약 표를 생성하여 outputs/object_contracts.json에 저장했습니다.
"""
