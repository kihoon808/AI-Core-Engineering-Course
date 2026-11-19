"""실습 01 Basic · Python 파일 하나로 원문을 수집합니다."""
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]))
from coursekit.io import DATA, save_json, show_success
from coursekit.documents import sha_bytes


def read_raw(path:Path)->bytes:
    """입력: Path / 출력: bytes. 원본 파일은 수정하지 않습니다."""
    # 1. 파일이 실제로 존재하는지 검증하여, 없는 파일 입력 시 빈 값으로 넘기지 않고 즉시 실패 처리
    if not path.is_file():
        raise FileNotFoundError(path)
    # 2. 텍스트 디코딩(UTF-8 등)은 다음 파싱 단계의 책임이므로, 수집 단계에서는 가공 없이 원본 바이트 그대로 읽기
    return path.read_bytes()
def build_record(doc_id:str,path:Path,raw:bytes)->dict:
    """파일명은 식별자가 아닙니다. 문서 ID와 원본 바이트 해시를 별도로 보관합니다."""
    # 1. 파일명은 변경되거나 중복될 수 있으므로, 시스템 내부 추적용 doc_id를 별도 키로 보관
    # 2. len(raw)는 텍스트 글자 수가 아닌 실제 바이트 크기이며, raw_sha256은 원본 변조 여부를 판별하는 지문 역할
    return {'doc_id':doc_id,'filename':path.name,'size_bytes':len(raw),
            'raw_sha256':sha_bytes(raw)}
def main():
    path=DATA/'raw'/'assignment.txt'
    raw=read_raw(path)
    record=build_record('DOC-ASSIGN',path,raw)
    assert record['size_bytes']==len(raw)
    out=save_json(HERE,'collection.json',record)
    show_success('01 Basic',out)

if __name__=='__main__':main()

"""
[실습 01 요약: 원문 수집(Document Collection)]
1. 데이터 수집 단계에서는 인코딩 변환이나 파싱을 섞지 않고 원본 파일을 순수 바이트(bytes) 상태로 읽어 무결성을 보존합니다.
2. 파일이 존재하지 않는 등 실패 지점은 빈 결과로 우회하지 않고 FileNotFoundError 예외를 발생시켜 명확히 차단합니다.
3. 파일명은 고유 식별자가 아니므로 문서 ID(doc_id), 바이트 크기(size_bytes), 원본 바이트의 SHA-256 해시값을 함께 기록해 데이터 추적과 변경 감지에 활용합니다.
"""
