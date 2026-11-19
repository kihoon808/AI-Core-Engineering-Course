"""실습 02 Basic · TXT parsing의 기본."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success


def decode_text(raw:bytes)->str:
    """errors='ignore'를 쓰면 누락을 탐지하기 어렵습니다."""
    # 1. Windows 환경 등에서 포함될 수 있는 UTF-8 BOM을 안전하게 제거하기 위해 'utf-8-sig' 사용
    # 2. errors='strict'(기본값)를 유지하여 손상된 바이트 입력 시 무시하지 않고 UnicodeDecodeError 발생
    return raw.decode('utf-8-sig')
def make_unit(doc_id:str,source_version:str,text:str)->dict:
    """TXT에는 페이지 번호가 없으므로 None. 가짜 page 1을 만들지 않습니다."""
    # 1. 텍스트 본문(raw_text)과 함께 문서 ID, 처리 버전(source_version), 단위 ID(unit_id), 파일 출처(source_locator)를 결합
    # 2. 일반 텍스트(TXT) 파일은 물리적 페이지 개념이 없으므로 page_number를 임의의 1이 아닌 None으로 명시
    return {'doc_id':doc_id,'source_version':source_version,
            'unit_id':'text-1','source_locator':'assignment.txt',
            'page_number':None,'raw_text':text}
def main():
    raw=(DATA/'raw'/'assignment.txt').read_bytes()
    text=decode_text(raw)
    if not text.strip():raise ValueError('empty text')
    unit=make_unit('DOC-ASSIGN','v1',text)
    out=save_json(HERE,'parsed_unit.json',unit)
    show_success('02 Basic',out)

if __name__=='__main__':main()

"""
[실습 02 요약: 문서 파싱(Document Parsing)]
1. 수집된 원본 바이트(bytes)를 UTF-8('utf-8-sig')로 엄격하게 디코딩하여, 잘못된 인코딩이나 손상된 문자를 은폐하지 않고 UnicodeDecodeError로 즉시 탐지합니다.
2. 파싱 결과물(ParsedUnit)에는 단순 본문(raw_text)뿐 아니라 문서 ID(doc_id), 버전(source_version), 단위 ID(unit_id), 출처(source_locator)를 함께 묶어 추적성을 확보합니다.
3. TXT 파일처럼 페이지 구분이 없는 포맷은 가짜 페이지 번호(예: 1)를 임의로 생성하지 않고 None(null)으로 명확히 표기합니다.
"""
