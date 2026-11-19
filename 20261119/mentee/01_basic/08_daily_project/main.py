"""실습 08 Basic · Checkpoint를 연결합니다. LLM 답변 생성은 하지 않습니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json,show_success
from coursekit.documents import by_doc,parse_one
from coursekit.processing import clean_prose,char_windows,build_chunk,validate_span


def run_pipeline(doc_id:str)->tuple[dict,str,list[dict]]:
    doc=by_doc(doc_id)
    result=parse_one(doc)
    if result['status']!='parsed':
        raise ValueError('parse not ready')
    unit=result['units'][0]
    # ParsedUnit의 원문 텍스트('raw_text')를 정제한 뒤 110자/15자 슬라이딩 윈도우로 청킹
    clean=clean_prose(unit['raw_text'])
    chunks=[build_chunk(doc,unit,clean,span)
            for span in char_windows(clean,110,15)]
    return doc,clean,chunks

def check_report(doc:dict,clean:str,chunks:list[dict])->dict:
    if not chunks:
        raise ValueError('empty chunk list')
    for c in chunks:
        if c['doc_id']!=doc['doc_id']:
            raise ValueError('doc_id mismatch')
        # Chunk의 본문('body')이 정제 본문의 [char_start, char_end) 슬라이스와 일치하는지 검증
        validate_span({'char_start':c['char_start'],'char_end':c['char_end'],
                       'text':c['body']},clean)
    # 실제 Embedding/DB 적재 전 단계이므로 'prepared_not_embedded'로 상태 명시
    return {'doc_id':doc['doc_id'],'status':'prepared_not_embedded',
            'chunk_count':len(chunks),'source_versions':[doc['source_version']],
            'chunk_ids':[c['chunk_id'] for c in chunks]}
def main():
    doc,clean,chunks=run_pipeline('DOC-ASSIGN')
    report=check_report(doc,clean,chunks)
    out=save_json(HERE,'daily_project.json',{'report':report,'chunks':chunks})
    show_success('08 Basic',out)

if __name__=='__main__':main()

"""
[실습 08 요약: Daily Project · 문서 처리 전체 파이프라인]
1. End-to-End 연결: 원문 조회(by_doc) -> 파싱(parse_one) -> 정제(clean_prose) -> 청킹(char_windows, build_chunk) -> 검증(validate_span)을 단일 흐름으로 결합합니다.
2. 무결성 검증 리포트: 모든 청크의 doc_id 일치 여부와 원문 Span 일치 여부를 검사한 뒤, 이상이 없을 때만 chunk_count와 chunk_ids를 리포트에 기록합니다.
3. 단계 구분: 임베딩/DB 적재가 완료되지 않은 준비 상태를 'prepared_not_embedded'로 명확히 구분해 허위 성공 보고를 방지합니다.
"""
