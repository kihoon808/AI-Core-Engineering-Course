"""내 PC에서 첫 요청 성공시키기. 실행: python -m uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Response

# BEGIN A01-01
# TODO A01-01: FastAPI 앱의 title을 Knowledge API로, description을 AI 플랫폼의 원본 지식 관리 연습으로 설정하세요.
# OpenAPI 메타데이터(Swagger 문서 타이틀 및 설명) 설정
app = FastAPI(title="Knowledge API", description="AI 플랫폼의 원본 지식 관리 연습")
# END A01-01

# HTTP GET 메서드와 /health 경로를 매핑하여 프로세스 생존 확인
@app.get("/health")
def health():
    # BEGIN A01-02
    # TODO A01-02: GET /health에서 status=ok인 dict를 반환하세요.
    # HTTP 200 상태코드 및 JSON 직렬화 응답 반환
    return {"status": "ok"}
    # END A01-02

# 쿼리 파라미터(Query Parameter)를 수신하는 GET 엔드포인트
@app.get("/hello")
def hello(name: str = "수강생"):
    # BEGIN A01-03
    # TODO A01-03: name을 포함한 안녕하세요, {name} 문자열을 message 값으로 반환하세요.
    # 쿼리 파라미터 값을 포맷팅하여 JSON 응답으로 반환
    return {"message": f"안녕하세요, {name}"}
    # END A01-03

"""
[핵심 개념 요약]
1. OpenAPI 메타데이터: FastAPI 생성자 파라미터(title, description)로 /docs Swagger 문서의 메타정보를 자동 구성합니다.
2. 쿼리 파라미터 자동 바인딩: 경로 변수에 없는 함수 인자는 URL 쿼리 스트링(?name=값)으로 자동 파싱되며 기본값을 지원합니다.
3. 자동 응답 직렬화: 핸들러가 반환한 Python dict는 별도 인코딩 없이 application/json 포맷(HTTP 200 OK)으로 직렬화됩니다.
"""

