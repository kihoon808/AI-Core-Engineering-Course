"""JSON 목록·상세 조회. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data

# ASGI 애플리케이션 생성 및 OpenAPI 메타데이터 등록
app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")

# 서버 헬스체크 엔드포인트 (Liveness 점검)
@app.get("/health")
def health():
    return {"status": "ok"}

# 지식 목록 전체 조회 엔드포인트 (컬렉션 Read)
@app.get("/api/knowledge")
def list_knowledge():
    with LOCK:
        data = read_data()
    # BEGIN B02-01
    # TODO B02-01: 파일 전체 data에서 entries 목록만 반환하세요. next_id가 포함된 dict 전체를 반환하지 마세요.
    # 서버 내부 관리 필드(next_id)를 제외하고 공개 데이터 목록(entries)만 반환
    return data["entries"]
    # END B02-01

# 특정 ID의 지식 단건 상세 조회 엔드포인트 (단일 리소스 Read)
@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        # BEGIN B02-02
        # TODO B02-02: 현재 entry의 id와 요청 knowledge_id가 같은지 비교하여 same_id에 저장하세요.
        # 경로 파라미터로 전달된 정수 ID와 저장소 항목의 ID 일치 여부 비교
        same_id = entry["id"] == knowledge_id
        # END B02-02
        if same_id:
            return entry
    # 조회 대상 ID가 존재하지 않을 경우 HTTP 404 예외 발생 (타입 불일치는 422 자동 반환)
    raise HTTPException(404, "Knowledge not found")

"""
[핵심 개념 요약]
1. 리소스 식별과 경로 파라미터: /api/knowledge/{id}처럼 URI 경로의 변수를 함수 인자(knowledge_id: int)로 자동 바인딩합니다.
2. 자동 타입 검증 및 422: int 타입 선언 시 숫자가 아닌 경로(/foo)는 Pydantic이 사전 차단하여 422 에러를 자동 응답합니다.
3. 내부 상태 캡슐화: 저장소 파일의 next_id 같은 서버 내부 관리용 메타데이터는 은닉하고 entries 데이터만 클라이언트에 전달합니다.
4. HTTP 404 상태코드: 리소스가 컬렉션에 존재하지 않는 예외 상황에는 HTTPException(404, ...)을 발생시켜 표준 에러를 반환합니다.
"""

