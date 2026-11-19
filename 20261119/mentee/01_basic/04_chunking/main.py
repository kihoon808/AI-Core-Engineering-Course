"""실습 04 Basic · 종료 조건이 중요한 문자 창."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success


def check_params(size:int,overlap:int)->None:
    # 1. type(...) is int로 검사: bool(True/False)은 int의 하위 타입이라 isinstance로는 걸러지지 않음
    # 2. 0 <= overlap < size 보장: overlap이 size 이상이면 다음 시작점이 전진하지 못해 무한 루프 발생
    if type(size) is not int or type(overlap) is not int or not (0<=overlap<size):
        raise ValueError('invalid chunk size or overlap')
def make_windows(text:str,size:int,overlap:int)->list[dict]:
    """본문 끝에서 반복문을 종료하지 않으면 겹친 꼬리 청크가 생깁니다."""
    # 1. 슬라이딩 윈도우 시작 전에 파라미터부터 검증
    check_params(size,overlap)
    spans=[]
    start=0
    # 2. 빈 문자열은 len(text)==0이라 반복문에 진입하지 않고 [] 반환
    while start<len(text):
        # 3. 마지막 청크는 본문 길이를 넘지 않도록 min으로 end를 제한, 범위는 [start,end) (끝 제외)
        end=min(start+size,len(text))
        spans.append({'char_start':start,'char_end':end,'text':text[start:end]})
        # 4. 창이 본문 끝에 닿으면 즉시 종료: 계속 돌면 이미 포함된 꼬리를 또 자른 중복 청크가 생김
        if end==len(text):
            break
        # 5. 다음 시작점은 현재 끝에서 overlap만큼 되돌아간 위치 (인접 청크가 overlap만큼 겹침)
        start=end-overlap
    return spans
def main():
    text='가'*71
    chunks=make_windows(text,size=40,overlap=10)
    assert [(c['char_start'],c['char_end']) for c in chunks]==[(0,40),(30,70),(60,71)]
    out=save_json(HERE,'chunks.json',{'source':'71-character teaching fixture','chunks':chunks})
    show_success('04 Basic',out)

if __name__=='__main__':main()

"""
[실습 04 요약: 청킹(Chunking)의 Size와 Overlap]
1. 문자 단위 슬라이딩 윈도우로 [start,end) 범위를 잘라 청크를 만들며, 다음 시작점은 end-overlap으로 되돌아가 인접 청크가 겹치게 합니다.
2. 0 <= overlap < size를 먼저 검증해야 합니다. overlap이 size 이상이면 시작점이 전진하지 못해 무한 루프에 빠지고, bool 입력은 type()으로 따로 거부합니다.
3. 창의 end가 본문 길이에 닿는 순간 반복을 종료해야 이미 포함된 꼬리를 다시 자른 중복 청크가 생기지 않습니다(71자 입력은 [0,40) [30,70) [60,71)).
"""
