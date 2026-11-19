"""실습 06 Basic · 본문과 설명 정보를 나눕니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json, show_success


def attach_metadata(chunk:dict,doc:dict)->dict:
    # 원문 문서(doc)로부터 출처 추적을 위한 핵심 메타데이터 필드들을 추출하여 청크(chunk) 딕셔너리에 병합 복사합니다.
    # - doc_id: 소속 원문 문서 고유 식별자
    # - source_version: 파이프라인 처리 및 원본 변경 추적 버전
    # - category: 필터링 및 도메인 분할용 분류 레이블
    # - source_locator: 원문 내 앵커/섹션/페이지 등 세부 위치 정보
    return {
        **chunk,
        'doc_id': doc['doc_id'],
        'source_version': doc['source_version'],
        'category': doc['category'],
        'source_locator': doc['source_locator'],
    }


def select_category(chunks:list[dict],category:str)->list[dict]:
    # 리스트 내 청크 중 지정된 category 속성과 일치하는 청크만 원래 순서를 보존(리스트 컴프리헨션)하여 필터링합니다.
    return [chunk for chunk in chunks if chunk['category'] == category]
def main():
    a=attach_metadata({'chunk_id':'C1','body':'출석 안내'},
                     {'doc_id':'DOC-ATTEND','source_version':'v1','category':'학사',
                      'source_locator':'attendance.md#sec-1'})
    b=attach_metadata({'chunk_id':'C2','body':'시설 안내'},
                     {'doc_id':'DOC-FACILITY','source_version':'v1','category':'시설',
                      'source_locator':'facility.html#main'})
    selected=select_category([a,b],'학사')
    assert [r['chunk_id'] for r in selected]==['C1']
    out=save_json(HERE,'metadata.json',{'total':2,'selected':selected})
    show_success('06 Basic',out)

if __name__=='__main__':main()

"""
[실습 06 핵심 개념 요약]
1. 메타데이터 바인딩: 청크 텍스트에 원본 문서 식별자(doc_id), 데이터 버전(source_version), 위치(source_locator)를 부착하여 인용(Citation) 추적성을 보장합니다.
2. 도메인 필터링: category 필드를 통해 특정 업무/분류 영역의 청크만을 안정적으로 선별하여 검색 범위 축소 및 오염 방지를 수행합니다.
3. 순서 보존: 원문 처리 순서가 유지된 채로 필터링을 수행함으로써 하위 검색 및 컨텍스트 재구성 단계에서 문맥의 일관성을 유지합니다.
"""
