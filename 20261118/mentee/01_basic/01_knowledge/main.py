"""Day23 실습 01 · 검색 대상과 ID (기본필수, mentee).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 3개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
from day23kit.data import load_knowledge
from day23kit.io import save_result

def select_original(rows):
    # 1. 101, 102, 103 ID에 해당하는 지식 데이터만 필터링
    # 2. 원본 데이터의 불변성을 보장하기 위해 dict(r)로 얕은 복사 수행
    # 3. ID 기준 오름차순(ascending) 정렬하여 반환
    return sorted((dict(r) for r in rows if r.get('id') in (101, 102, 103)), key=lambda r: r['id'])

def make_passage_input(row):
    # E5 비대칭 검색 규격: 검색 문서(문맥)에는 'passage: ' 접두어를 부여하고 제목과 본문을 단일 공백으로 연결
    return f"passage: {row['title']} {row['content']}"

def make_mapping(rows):
    # 벡터 생성 전 원문 메타데이터(id, title, content, category, source_version)와
    # 생성된 passage_input을 함께 유지하여 데이터 추적성을 확보
    return [
        {
            'id': r['id'],
            'title': r['title'],
            'content': r['content'],
            'category': r['category'],
            'source_version': r['source_version'],
            'passage_input': make_passage_input(r),
        }
        for r in rows
    ]

def run(mode,level,args):
    rows=load_knowledge()
    selected=select_original(rows)
    passage=make_passage_input(selected[1])
    mapping=make_mapping(selected if level==1 else rows)
    result=dict(exercise=1,level=level,source_mode='local_snapshot',
                selected_ids=[r['id'] for r in selected],example_passage=passage,
                total_mapped=len(mapping),mapping=mapping)
    if level>=2:
        result['unique_ids']=len(reject_duplicate_ids(rows))
        result['all_fields_valid']=reject_missing_fields(rows)
    if level>=3:
        result['versions']=audit_versions(rows)
    return result


def main():
    parser=argparse.ArgumentParser(description='Day23 실습 01 · 검색 대상과 ID')
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    args=parser.parse_args()
    result=run(args.mode,1,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_01.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
