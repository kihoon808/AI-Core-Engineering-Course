"""내 PC에서 첫 요청 성공시키기. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response

# ASGI 웹 애플리케이션 인스턴스 생성 및 OpenAPI 메타데이터 설정
app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")

# HTTP GET 메서드와 /health 경로를 핸들러 함수에 매핑
@app.get("/health")
def health():
    # 서버 프로세스 생존 확인(Liveness Probe)용 엔드포인트
    # BEGIN B01-01
    # TODO B01-01: status 키의 값이 ok인 dict를 반환하세요. GET /health의 본문은 {"status":"ok"}여야 합니다.
    # dict 반환 시 FastAPI가 HTTP 200 상태코드와 application/json으로 자동 직렬화
    return {"status": "ok"}
    # END B01-01

"""
[핵심 개념 요약]
1. ASGI & Uvicorn: FastAPI 인스턴스는 비동기 서버인 Uvicorn에 의해 구동되어 클라이언트 요청을 디스패치합니다.
2. 자동 JSON 직렬화: 핸들러가 Python dict를 반환하면 프레임워크가 Content-Type: application/json 및 200 OK로 자동 변환합니다.
3. Liveness 점검 및 문서화: /health로 서버 가동 여부를 단순 점검하며, /docs 및 /openapi.json 문서를 자동 생성합니다.
"""