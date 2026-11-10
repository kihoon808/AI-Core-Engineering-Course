"""JSON 목록·상세 조회. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data

# ASGI 애플리케이션 생성 및 메타데이터 등록
app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")

# 서버 생존 확인 엔드포인트
@app.get("/health")
def health():
    return {"status": "ok"}

# 쿼리 파라미터 기본값 처리 엔드포인트
@app.get("/hello")
def hello(name: str = "수강생"):
    return {"message": f"안녕하세요, {name}"}

# 카테고리 필터링을 지원하는 지식 목록 조회 엔드포인트 (Query Param)
@app.get("/api/knowledge")
def list_knowledge(category: str | None = None):
    with LOCK:
        data = read_data()
    result = data["entries"]
    if category is not None:
        # BEGIN A02-01
        # TODO A02-01: category와 정확히 일치하는 항목만 result에 남기세요. 일치 항목이 없으면 빈 목록이어야 합니다.
        # 선택적 쿼리 파라미터와 카테고리가 일치하는 항목만 리스트 컴프리헨션으로 필터링
        result = [entry for entry in result if entry["category"] == category]
        # END A02-01
    # 조건에 맞는 지식이 없으면 정상 조회 200과 빈 배열 []입니다.
    return result

# 지식 단건 상세 조회 엔드포인트 (Path Param)
@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    # BEGIN A02-02
    # TODO A02-02: entries를 순회하여 id가 knowledge_id인 지식을 반환하세요. 찾지 못하면 반복문 다음으로 진행하세요.
    # 전체 항목을 순회하며 ID가 일치하는 항목을 조기 반환(Early Return)
    for entry in data["entries"]:
        if entry["id"] == knowledge_id:
            return entry
    # END A02-02
    # BEGIN A02-03
    # TODO A02-03: 반복문에서 찾지 못한 경우 HTTPException으로 404와 Knowledge not found를 전달하세요.
    # 대상 ID를 찾지 못한 경우 404 상태코드와 에러 메시지를 담은 HTTPException 발생
    raise HTTPException(404, "Knowledge not found")
    # END A02-03

"""
[핵심 개념 요약]
1. 선택적 쿼리 필터링: category: str | None = None으로 쿼리 파라미터를 받아 일치 항목만 선별하며, 미일치 시 빈 리스트([])와 200 OK를 반환합니다.
2. 조기 반환(Early Return): 리스트 탐색 중 일치하는 식별자(ID)를 찾으면 즉시 return하여 불필요한 연산을 방지합니다.
3. HTTPException 명시적 발생: 리소스 부재 시 return이 아닌 raise HTTPException(404, ...)으로 파이프라인을 즉시 중단하고 클라이언트에 404를 응답합니다.
"""

