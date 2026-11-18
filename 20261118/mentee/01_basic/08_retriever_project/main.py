"""Day23 실습 08 · AI Agent용 Retriever (기본필수, mentee).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 3개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
from time import perf_counter
from day23kit.fixtures import fixture_search
from day23kit.embedding import get_encoder, encode_question
from day23kit.db import connect_db, exact_topk, check_data_ready
from day23kit.io import save_result

def validate_question(question):
    # 질문 입력 유효성 검증(문자열 여부, 빈 공백 여부) 및 공백 제거
    if not isinstance(question, str) or not question.strip():
        raise ValueError('empty_question')
    return question.strip()

def retrieve_candidates(question, mode, k, category, env_file):
    # 실행 모드에 따라 모의 검색(fixture) 또는 E5 임베딩 기반 pgvector 실측 검색 수행
    if mode == 'fixture':
        return fixture_search(question, k, category)
    encoder = get_encoder('live')
    qvec = encode_question(encoder, question)
    with connect_db(env_file) as conn:
        check_data_ready(conn)
        return exact_topk(conn, qvec, k, category)

def format_candidates(hits):
    # 검색된 후보 문서들의 원문 메타데이터 및 코사인 거리를 규격화하여 반환
    return [{'id': h['id'], 'title': h['title'], 'content': h['content'],
             'category': h['category'], 'source_version': h['source_version'],
             'distance': round(float(h['distance']), 6)} for h in hits]

def run(mode,level,args):
    question=validate_question(getattr(args,'question','서버는 어디에서 실행하나요?'))
    k=3 if level==1 else args.k
    category=None if level==1 else args.category
    if level>=2:options=validate_options(k,category)
    else:options={'k':k,'category':category}
    t0=perf_counter()
    hits=retrieve_candidates(question,mode,options['k'],options['category'],Path(__file__).with_name('.env'))
    elapsed=(perf_counter()-t0)*1000
    formatted=format_candidates(hits)
    result=dict(exercise=8,level=level,source_mode='simulated' if mode=='fixture' else 'pgvector_exact',question=question,options=options,
                retrieved=formatted,retrieved_count=len(formatted),human_evidence_ok=None,
                next_step='검토 후 Context 후보로 전달; LLM 답변 생성은 Day25 RAG에서 수행')
    if level>=2:result['run_report']=make_run_report(question,hits,mode,elapsed)
    if level>=3:result['contract_check']=check_model_and_versions(hits,mode)
    return result

def main():
    parser=argparse.ArgumentParser(description='Day23 실습 08 · AI Agent용 Retriever')
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')

    parser.add_argument('--question',default='서버는 어디에서 실행하나요?',help='검색 질문')
    parser.add_argument('--k',type=int,default=3,help='반환할 최대 검색 후보 (1~9)')
    parser.add_argument('--category',default=None,choices=['course','development','support'],help='Metadata 분류 필터')
    args=parser.parse_args()
    result=run(args.mode,1,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_08.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
