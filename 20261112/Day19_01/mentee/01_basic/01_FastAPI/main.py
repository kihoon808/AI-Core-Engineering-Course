from fastapi import FastAPI, HTTPException, Response
from storage import LOCK, read_data, write_data

from pydantic import BaseModel, Field


class KnowledgeWrite(BaseModel):
    # 세 필드는 모두 필수입니다. 길이 규칙은 공백 제거 규칙과 다릅니다.
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=2000)
    category: str = Field(min_length=1, max_length=30)


class Knowledge(KnowledgeWrite):
    id: int

app = FastAPI(title="Day19 AM Knowledge API - Basic")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/knowledge", response_model=list[Knowledge])
def list_knowledge():
    with LOCK:
        data = read_data()
    # BEGIN B-API-01
    # [설명 B-API-01]: 저장소의 전체 JSON 구조 중 사용자용 entries 목록을 id 기준 오름차순으로 정렬하여 반환합니다.
    # next_id는 새로운 항목 생성 시 발급할 식별자 내부 상태이므로 클라이언트 응답에 포함하지 않습니다.
    return sorted(data["entries"], key=lambda e: e["id"])
    # END B-API-01
@app.get("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def get_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
    for entry in data["entries"]:
        # BEGIN B-API-02
        # [설명 B-API-02]: entries 목록을 순회하며 대상 knowledge_id와 일치하는 id를 가진 항목을 반환합니다.
        # 배열 순서(인덱스)와 고유 식별자(id)는 삭제나 정렬에 의해 달라질 수 있으므로 entry["id"]를 비교합니다.
        if entry["id"] == knowledge_id:
            return entry
        # END B-API-02
    raise HTTPException(404, "Knowledge not found")

@app.post("/api/knowledge", status_code=201, response_model=Knowledge)
def create_knowledge(payload: KnowledgeWrite):
    with LOCK:
        data = read_data()
        # BEGIN B-API-03
        # [설명 B-API-03]: 클라이언트가 전송한 payload를 dict로 변환하고, 저장소의 next_id를 발급받아 id 필드로 할당합니다.
        entry = payload.model_dump()
        entry["id"] = data["next_id"]
        # END B-API-03
        # BEGIN B-API-04
        # [설명 B-API-04]: 생성된 entry를 entries에 추가하고 next_id를 1 증가시킨 뒤 write_data(data)로 파일에 영구 저장합니다.
        # 항목 삭제 후에도 ID 중복을 방지하기 위해 len(entries)+1 대신 단조 증가하는 next_id를 사용합니다.
        data["entries"].append(entry)
        data["next_id"] += 1
        write_data(data)
        # END B-API-04
    return entry

@app.put("/api/knowledge/{knowledge_id}", response_model=Knowledge)
def update_knowledge(knowledge_id: int, payload: KnowledgeWrite):
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                updated = payload.model_dump()
                updated["id"] = knowledge_id
                # BEGIN B-API-05
                # [설명 B-API-05]: 찾은 위치 i의 기존 항목을 수정된 updated 내용으로 교체하고 파일에 반영합니다.
                # 기존 id는 동일하게 유지되며 다른 항목이나 next_id는 변경되지 않습니다.
                data["entries"][i] = updated
                write_data(data)
                # END B-API-05
                return updated
    raise HTTPException(404, "Knowledge not found")

@app.delete("/api/knowledge/{knowledge_id}", status_code=204)
def delete_knowledge(knowledge_id: int):
    with LOCK:
        data = read_data()
        for i, entry in enumerate(data["entries"]):
            if entry["id"] == knowledge_id:
                # BEGIN B-API-06
                # [설명 B-API-06]: 대상 항목을 pop(i)로 entries 목록에서 제거한 후 파일에 저장합니다.
                # 이미 부여된 다른 항목들의 id와의 충돌 방지를 위해 next_id는 감소시키지 않습니다.
                data["entries"].pop(i)
                write_data(data)
                # END B-API-06
                return Response(status_code=204)
    raise HTTPException(404, "Knowledge not found")
