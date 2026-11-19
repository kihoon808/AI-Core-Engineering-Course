"""실습 07 Basic · 기본 실행은 데이터 계약, --live-db는 실제 E5/DB 실행."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json, show_success
from coursekit.documents import by_doc,parse_one
from coursekit.processing import make_chunks


def select_index_chunk(doc_id:str)->tuple[dict,dict]:
    doc=by_doc(doc_id)
    parsed=parse_one(doc)
    if parsed['status']!='parsed':
        raise ValueError('not indexable')
    chunks=make_chunks(doc,parsed['units'][0],size=110,overlap=15)
    # 첫 번째 유효 Chunk를 선택하고 E5 본문 접두어('passage: ')가 붙어 있는지 확인
    first=chunks[0]
    if not first['body'].strip() or not first['embedding_text'].startswith('passage: '):
        raise ValueError('bad embedding input')
    return doc,first

def format_hit(row:tuple)->dict:
    """DB 행: citation_id,chunk_id,body,locator,doc_id,version,distance."""
    cid,chunk_id,body,locator,doc_id,source_version,distance=row
    # DB의 citation_id는 양의 정수(int)여야 하며 bool 등 비정상 타입/0 이하 값은 거부
    if type(cid) is not int or cid<=0:
        raise ValueError('invalid citation ID')
    return {'citation_id':cid,'chunk_id':chunk_id,'body':body,
            'source_locator':locator,'doc_id':doc_id,
            'source_version':source_version,'cosine_distance':float(distance)}
def main():
    doc,chunk=select_index_chunk('DOC-ASSIGN')
    output={'source_mode':'prepared_only_not_db','chunk':chunk,
            'live_db':'not_run','sample_hit_contract':format_hit((201,chunk['chunk_id'],chunk['body'],chunk['source_locator'],doc['doc_id'],'v1',0.0))}
    if '--live-db' in sys.argv:
        from coursekit.live import connect_db,load_encoder,encode_passages,encode_query
        from coursekit.db import initialize,stage_version,publish_version,search_current,use_schema
        # 실제 모델 추론은 DB 트랜잭션 전에 수행합니다.
        model=load_encoder();vectors=encode_passages(model,[chunk])
        query=encode_query(model,'과제 파일은 어디에 보관하나요?')
        with connect_db() as conn:
            use_schema(conn,'d24_basic07')
            initialize(conn)
            with conn.transaction():
                stage_version(conn,doc,doc['file'],[chunk],vectors)
                publish_version(conn,doc['doc_id'],doc['source_version'],chunk['pipeline_version'])
            result=search_current(conn,query,category='학사',k=3)
            output['source_mode']='e5_pgvector_live'
            output['live_db']=[format_hit(r) for r in result]
    out=save_json(HERE,'indexing.json',output)
    show_success('07 Basic',out)

if __name__=='__main__':main()

"""
[실습 07 요약: pgvector Indexing 및 검색 결과 계약]
1. 임베딩 입력 준비: 파싱·정제·청킹된 본문에 E5 문서 접두어('passage: ')가 올바르게 붙어 있는지 검증하여 잘못된 벡터 생성을 막습니다.
2. 검색 결과 정규화: DB에서 반환된 행(tuple)을 정수형 citation_id(1 이상), chunk_id, 본문, 출처(source_locator), cosine_distance(float)의 구조화된 딕셔너리로 변환합니다.
3. 실행 상태 분리: DB 미연결 기본 실행은 'prepared_only_not_db' / 'not_run'으로 기록하여 준비 완료와 실제 DB 적재 성공을 혼동하지 않습니다.
"""
