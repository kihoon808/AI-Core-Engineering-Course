"""B-12: FastAPI는 요청을 받고 서비스 결과를 반환한다."""
from uuid import uuid4
from fastapi import APIRouter,Request
from app.schemas.agent import AskRequest,AskResponse
from app.services.metrics import Meter
from app.services.errors import ServiceError

router=APIRouter(prefix='/api/v1')
@router.post('/agent/ask',response_model=AskResponse)
def ask(body:AskRequest,request:Request):
    runtime=request.app.state.get_runtime()
    runtime.health()
    request_id=str(uuid4());meter=Meter(runtime.settings)
    # 요청 단위 Meter와 함께 AgentService 실행 결과(AskResponse) 반환
    return runtime.agent.ask(request_id, body, meter)


"""
[코드 요약]
- POST /api/v1/agent/ask 요청에 대해 Runtime 건강 상태를 먼저 확인하고 요청별 request_id와 Meter를 생성한다.
- runtime.agent.ask(request_id, body, meter)를 호출해 검증된 AskResponse 계약 형태로 응답을 반환한다.
"""
