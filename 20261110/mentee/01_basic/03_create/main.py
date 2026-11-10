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

@app.get("/api/knowledge")
def list_knowledge():
    with LOCK:
        data = read_data()
    # 파일 전체에는 내부용 next_id도 있으므로 entries만 응답합니다.
    return data["entries"]

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
        entry = payload.model_dump()
        entry["id"] = data["next_id"]
        # BEGIN B03-01
        # TODO B03-01: 새 entry를 data 안의 entries 목록 끝에 한 번 추가하세요.
        # 메모리 목록 끝에 새 데이터 항목 추가
        data["entries"].append(entry)
        # END B03-01
        # BEGIN B03-02
        # TODO B03-02: 다음 생성에 쓸 next_id 값을 1 증가시키세요.
        # 중복 방지를 위한 다음 발급용 식별자 1 증가
        data["next_id"] += 1
        # END B03-02
        # BEGIN B03-03
        # TODO B03-03: 변경된 data 전체를 write_data에 전달해 저장하세요. LOCK 블록 안에서 호출하세요.
        # 변경된 상태를 JSON 파일에 영구 기록
        write_data(data)
        # END B03-03
    # HTTP 201 Created 응답과 함께 생성된 리소스 반환
    return entry

"""
[핵심 개념 요약]
1. Pydantic 스키마 검증: 요청 바디(HTTP Body)를 KnowledgeWrite 모델로 자동 역직렬화 및 유효성(길이 제약)을 사전 검증합니다.
2. 서버 주도 ID 발급: 클라이언트 입력이 아닌 서버 저장소의 next_id를 기반으로 고유 식별자를 부여하여 무결성을 보장합니다.
3. 동시성 제어(LOCK): 멀티스레드 환경에서 읽기-수정-쓰기(RMW) 경쟁 상태(Race Condition)를 Lock으로 원자화합니다.
4. HTTP 201 상태코드: 리소스 신규 생성 완료 시 상태코드 201과 response_model 규격에 맞춘 생성 객체를 반환합니다.
"""

