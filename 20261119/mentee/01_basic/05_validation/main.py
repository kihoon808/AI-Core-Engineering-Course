"""실습 05 Basic · 유효한 위치인지 먼저 판단."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import save_json, show_success


def check_bounds(chunk:dict,text:str)->None:
    # 청크의 시작 인덱스와 종료 인덱스를 추출합니다.
    start = chunk['char_start']
    end = chunk['char_end']
    
    # 인덱스가 정수형인지 확인하고, 유효한 반열린 구간 [start, end)인지 검증합니다.
    # 조건: 0 <= start < end <= len(text) (역전 구간이나 본문 범위 초과 방지)
    if type(start) is not int or type(end) is not int or not (0 <= start < end <= len(text)):
        raise ValueError('invalid span')


def check_content(chunk:dict,text:str)->None:
    # 1단계: 청크의 인덱스 경계가 본문 전체 범위 내에서 유효한지 사전 검증합니다.
    check_bounds(chunk, text)
    
    # 2단계: 청크에 기록된 text가 정제 본문의 슬라이스 구간(text[start:end])과 정확히 일치하는지 확인합니다.
    # 불일치 시 인덱스 변조 또는 텍스트 오염으로 간주합니다.
    if chunk['text'] != text[chunk['char_start']:chunk['char_end']]:
        raise ValueError('span text mismatch')
    
    # 3단계: 공백이나 줄바꿈 문자로만 이루어진 무의미한 빈 청크인지 검증합니다.
    if not chunk['text'].strip():
        raise ValueError('empty content')
def main():
    text='10분 초과 시 결석으로 기록합니다.'
    good={'char_start':0,'char_end':len(text),'text':text}
    bad={'char_start':0,'char_end':len(text),'text':'잘못된 내용'}
    check_content(good,text)
    try:check_content(bad,text)
    except ValueError:result='expected failure'
    else:raise AssertionError('a corrupted chunk must fail')
    out=save_json(HERE,'span_check.json',{'good':'pass','bad':result})
    show_success('05 Basic',out)

if __name__=='__main__':main()

"""
[실습 05 핵심 개념 요약]
1. Span 검증: 청크가 원문 텍스트 내에서 올바른 반열린 구간 [char_start, char_end)을 가리키는지 확인합니다 (0 <= start < end <= len(text)).
2. 내용 무결성: 청크의 본문 텍스트(chunk['text'])가 원문의 해당 슬라이스 구간과 1바이트의 오차도 없이 일치하는지 검증합니다.
3. 유효성 게이트: 공백만으로 구성된 빈 청크나 잘못된 오프셋을 조기에 차단하여 벡터 임베딩 및 검색 인덱스의 오염을 방지합니다.
"""
