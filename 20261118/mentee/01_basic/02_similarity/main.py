"""Day23 실습 02 · Vector·Similarity·Distance (기본필수, mentee).

실행: python main.py --mode fixture
실제 E5/DB: python main.py --mode live  (필요한 선행 설치 후)
수강생 TODO: 3개 / 상세 요구사항은 각 함수의 주석 및 README.md.
fixture는 모의 시연이지 모델·PostgreSQL 실측 결과가 아닙니다.
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2] / 'common'))
import numpy as np
from day23kit.mathops import cosine_distance
from day23kit.io import save_result


def dot(a,b):
    # 대응하는 좌표 원소끼리 곱한 뒤 합산 (내적 계산)
    return float(np.dot(a,b))

def cosine(a,b):
    # 두 벡터의 L2 노름(길이) 계산
    na=float(np.linalg.norm(a))
    nb=float(np.linalg.norm(b))
    # 영벡터 입력 시 0으로 나누기 오류 방지
    if na<=1e-12 or nb<=1e-12:raise ValueError('zero_vector')
    # 내적을 두 벡터 길이의 곱으로 나누어 코사인 유사도 산출
    return dot(a,b)/(na*nb)

def l2(a,b):
    # 좌표 간 차이 벡터의 L2 노름(유클리드 거리) 계산
    return float(np.linalg.norm(a-b))

def run(mode,level,args):
    q=np.array([1.,0.]);a=np.array([.8,.6]);u=np.array([1.,0.]);v=np.array([10.,10.])
    result=dict(exercise=2,level=level,source_mode='local_math',
                dot=round(dot(q,a),6),cosine=round(cosine(q,a),6),l2=round(l2(q,a),6),
                cosine_distance=round(1-cosine(q,a),6))
    if level>=2:
        result['normalized_v']=normalize(v).round(6).tolist()
        result['rankings']=rank_dot_vs_cosine(q,{'U':u,'V':v})
    if level>=3:
        result['validated']=validate_pair(q,a)
        errors={}
        for label,x,y in [('dimension_mismatch',q,np.array([1.,0.,2.])),
                           ('nonfinite',q,np.array([np.nan,1.])),
                           ('zero_vector',q,np.array([0.,0.]))]:
            try:validate_pair(x,y)
            except ValueError as e:errors[label]=str(e)
        result['invalid_inputs']=errors
    return result


def main():
    parser=argparse.ArgumentParser(description='Day23 실습 02 · Vector·Similarity·Distance')
    parser.add_argument('--mode',choices=['fixture','live'],default='fixture',
        help='fixture=모의 벡터/오프라인, live=실제 E5/DB가 필요한 단계')
    args=parser.parse_args()
    result=run(args.mode,1,args)
    path=save_result(Path(__file__).resolve().parent,'exercise_02.json',result)
    import json
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
    print('결과 저장:',path)

if __name__=='__main__':
    main()
