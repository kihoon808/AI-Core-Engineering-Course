"""안내문 등록과 파일 저장. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data

from pydantic import BaseModel, Field

# 입력 모델은 HTTP Body의 규칙입니다. DB 테이블이나 저장 코드가 아닙니다.
class KnowledgeWrite(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=2000)
    category: str = Field(min_length=1, max_length=30)


class Knowledge(KnowledgeWrite):
    id: int


app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")

@app.get("/health")
def health():
    # 이 경로의 응답 확인입니다. 파일·DB·AI 모델의 전체 상태 점검은 아닙니다.
    return {"status": "ok"}

@app.get("/hello")
def hello(name: str = "수강생"):
    return {"message": f"안녕하세요, {name}"}

@app.get("/api/knowledge")
def list_knowledge(category: str | None = None):
    with LOCK:
        data = read_data()
    result = data["entries"]
    if category is not None:
        result = [entry for entry in result if entry["category"] == category]
    # 조건에 맞는 지식이 없으면 정상 조회 200과 빈 배열 []입니다.
    return result

@app.get("/api/knowledge/{knowledge_id}")
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        same_id = entry["id"] == knowledge_id
        if same_id:
            return entry
    # 입력은 정수이지만 저장된 항목이 없으면 404입니다. foo 같은 Path는 먼저 422입니다.
    raise HTTPException(404, "Knowledge not found")

@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    # 동시성 충돌 방지를 위한 임계 구역 잠금(Lock) 획득
    with LOCK:
        data = read_data()
        # BEGIN A03-01
        # TODO A03-01: 검증된 payload를 dict로 변환하여 entry에 저장하세요.
        # Pydantic 모델을 딕셔너리로 직렬화
        entry = payload.model_dump()
        # END A03-01
        # BEGIN A03-02
        # TODO A03-02: 현재 data의 next_id를 새 entry의 id로 지정하세요.
        # 서버 관리 시퀀스로부터 고유 식별자(ID) 부여
        entry["id"] = data["next_id"]
        # END A03-02
        # BEGIN A03-03
        # TODO A03-03: entries에 새 지식을 추가한 뒤 다음 ID를 1 올리세요.
        # 메모리 컬렉션에 추가 및 다음 ID 증가
        data["entries"].append(entry)
        data["next_id"] += 1
        # END A03-03
        # BEGIN A03-04
        # TODO A03-04: 변경된 data를 파일에 저장하세요.
        # 원자적 파일 쓰기 수행
        write_data(data)
        # END A03-04
    # HTTP 201 Created 응답과 함께 생성된 리소스 반환
    return entry

"""
[핵심 개념 요약]
1. Pydantic 스키마 검증: 요청 바디(HTTP Body)를 KnowledgeWrite 모델로 자동 역직렬화 및 유효성(길이 제약)을 사전 검증합니다.
2. 서버 주도 ID 발급: 클라이언트 입력이 아닌 서버 저장소의 next_id를 기반으로 고유 식별자를 부여하여 무결성을 보장합니다.
3. 동시성 제어(LOCK): 멀티스레드 환경에서 읽기-수정-쓰기(RMW) 경쟁 상태(Race Condition)를 Lock으로 원자화합니다.
4. HTTP 201 상태코드: 리소스 신규 생성 완료 시 상태코드 201과 response_model 규격에 맞춘 생성 객체를 반환합니다.
"""

