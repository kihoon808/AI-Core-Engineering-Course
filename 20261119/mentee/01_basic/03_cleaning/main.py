"""실습 03 Basic · 일반 prose 전용 cleaning."""
from pathlib import Path
import re,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success


def unify_newlines(text:str)->str:
    # 1. Windows(CRLF, \r\n)와 구형 Mac(CR, \r) 줄바꿈을 LF(\n)로 통일
    # 2. 반드시 CRLF를 먼저 치환해야 함: CR을 먼저 바꾸면 \r\n이 \n\n(빈 줄 1개 추가)으로 변질됨
    # 3. 줄을 합치지 않으므로 문단 경계(빈 줄)는 그대로 보존
    return text.replace('\r\n','\n').replace('\r','\n')
def reduce_horizontal_spaces(text:str)->str:
    """줄 단위 변환이므로 빈 줄이 사라지지 않습니다."""
    # 1. text.split('\n')으로 줄 단위 분리: 줄 경계를 건드리지 않아 빈 줄(문단 구분)이 유지됨
    # 2. 각 줄에서 연속된 공백/탭([ \t]+)을 한 칸으로 줄이고 좌우 공백 제거(strip)
    # 3. 전체 결과의 앞뒤 공백/빈 줄은 마지막 strip()으로 정리
    return '\n'.join(re.sub(r'[ \t]+',' ',line).strip()
                     for line in text.split('\n')).strip()
def main():
    text='출석   안내\r\n\r\n10분  초과는 결석.\r\n단,  사전 승인 시 예외.'
    cleaned=reduce_horizontal_spaces(unify_newlines(text))
    assert '10분 초과는 결석.' in cleaned
    assert '\n\n' in cleaned
    out=save_json(HERE,'cleaning.json',{'before':repr(text),'after':cleaned})
    show_success('03 Basic',out)

if __name__=='__main__':main()

"""
[실습 03 요약: 일반 문장(prose) 정제(Cleaning)]
1. 줄바꿈은 CRLF를 먼저, CR을 나중에 LF로 치환해 OS별 차이를 통일하되, 줄을 합치지 않아 문단 경계(빈 줄)를 보존합니다.
2. 공백 정리는 전체 문자열이 아닌 줄 단위(split('\\n'))로 수행하므로, 줄 안의 연속 공백/탭만 한 칸으로 줄이고 빈 줄은 사라지지 않습니다.
3. 이 규칙은 일반 prose 전용입니다. 코드 들여쓰기나 표의 탭 구분에 적용하면 구조가 깨지므로 문서 유형에 맞춰 정제 규칙을 선택해야 합니다.
"""
