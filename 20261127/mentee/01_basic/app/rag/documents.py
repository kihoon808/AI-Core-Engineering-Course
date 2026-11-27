"""B-06: 실제 VIEW 원문을 LangChain Document와 Metadata로 보존."""
from langchain_core.documents import Document
from app.services.errors import ServiceError

def to_document(row):
    # 검색용 overview와 답변 근거용 content를 분리해 Document와 metadata에 저장
    return Document(
        page_content=row['content'],
        metadata={
            'source_id': f"RPT-{row['report_id']}",
            'report_id': row['report_id'],
            'title': row['title'],
            'category_code': row['category_code'],
            'revision': row['revision'],
            'overview': row['overview'],
            'distance': float(row['distance']),
        },
    )

def source_of(doc):
    return {k:doc.metadata[k] for k in ('source_id','report_id','title','category_code','revision')}
