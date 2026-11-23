"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
from coursekit.io import save_json, show_success
from coursekit.data import example_hit, load_hits
from coursekit.reporting import execution_record
from langchain_core.documents import Document
import argparse

# 오늘의 최소 Metadata 계약. 여섯 값 모두 입력 Hit에서 가져옵니다.
METADATA_KEYS = ("citation_id", "chunk_id", "doc_id", "source_version", "source_locator", "category")

# 단일 검색 결과(hit)의 본문과 6개 필수 메타데이터를 LangChain Document로 변환
def to_document(hit: dict) -> Document:
    """한 Hit의 본문과 여섯 Metadata 값을 Document로 옮깁니다."""
    return Document(
        page_content=hit["body"],
        metadata={key: hit[key] for key in METADATA_KEYS},
    )

# 검색 결과 목록을 입력 순서대로 Document 리스트로 변환 (빈 입력 시 빈 리스트 반환)
def hits_to_documents(hits: list[dict]) -> list[Document]:
    """순서대로 변환한 Document 목록을 반환합니다. 빈 입력은 빈 목록입니다."""
    return [to_document(hit) for hit in hits]

def metadata_is_preserved(hit: dict, metadata: dict) -> bool:
    """제공된 관찰 함수: 여섯 필드가 모두 있고 각 값이 같은지 확인합니다."""
    required = {"citation_id", "chunk_id", "doc_id", "source_version", "source_locator", "category"}
    # 일부 필드만 복사한 결과를 '보존 완료'로 표시하지 않도록 Key 집합부터 확인합니다.
    return set(metadata) == required and all(metadata[key] == hit[key] for key in required)


def main():
    parser = argparse.ArgumentParser(description="Hit → 실제 LangChain Document 변환")
    parser.add_argument("--live-db", action="store_true", help="실제 E5·PostgreSQL 검색 결과를 입력으로 사용")
    parser.add_argument("--question", default="15분 늦으면 어떻게 기록되나요?")
    parser.add_argument("--category", default="학사", choices=["학사", "시설", "지원"])
    parser.add_argument("--candidate-k", type=int, default=3)
    args = parser.parse_args()
    if args.live_db:
        # --live-db를 선택한 경우에만 실제 모델·DB 준비 함수를 불러옵니다.
        from coursekit.live import make_search_hits
        search_hits = make_search_hits()
        hits = search_hits(args.question, args.category, k=args.candidate_k)
        mode, input_source = "live_db", "E5_PostgreSQL"
    else:
        hits = [example_hit()]
        mode, input_source = "local_adapter", "lecture_fixture"
    documents = hits_to_documents(hits)
    comparisons = []
    for hit, doc in zip(hits, documents):
        comparisons.append({
            "citation_id": doc.metadata["citation_id"],
            "body_preserved": doc.page_content == hit["body"],
            "metadata_preserved": metadata_is_preserved(hit, doc.metadata),
            "citation_id_type": type(doc.metadata["citation_id"]).__name__,
            "page_content": doc.page_content,
            "metadata": doc.metadata,
        })
    report = {
        "execution": execution_record(mode, db=args.live_db, embedding=args.live_db),
        "input_source": input_source,
        "input_count": len(hits), "document_count": len(documents),
        "documents": comparisons,
    }
    path = save_json(HERE, "document_adapter.json", report)
    show_success("04 기본필수", path)

if __name__ == "__main__":
    main()

"""
[실습 04 요약]
- 검색 결과(hit dict)의 본문(body)을 page_content로, 6개 필수 출처 필드를 metadata로 옮겨 LangChain Document 객체를 생성했습니다.
- hits_to_documents는 입력 순서를 유지하며 변환하고, 빈 목록 입력 시 빈 목록을 그대로 반환합니다.
- 변환된 Document의 본문·메타데이터 보존 여부와 citation_id 타입(int)을 검증해 outputs/document_adapter.json에 저장했습니다.
"""
