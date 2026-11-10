"""외부 접속 공유용 FastAPI 서버
실행: python -m uvicorn demo_server:app --host 0.0.0.0 --port 8000 --reload
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="조기훈 서버", description="20261110 FastAPI 외부 공유 실습")

# 브라우저 기본 접속 시(루트 경로) HTML 화면 반환
@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>조기훈 서버</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f1f5f9;
            }
            .card {
                background: white;
                padding: 2.5rem;
                border-radius: 1rem;
                box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                text-align: center;
                max-width: 400px;
                width: 90%;
            }
            h1 {
                color: #0f172a;
                margin-top: 0;
                font-size: 1.6rem;
            }
            p {
                color: #475569;
                font-size: 1rem;
                margin-bottom: 1.5rem;
            }
            .badge {
                display: inline-block;
                background: #e0f2fe;
                color: #0284c7;
                padding: 0.35rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.875rem;
                font-weight: 600;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">FastAPI Live</span>
            <h1>안녕하세요 조기훈입니다</h1>
            <p>2026-11-10 실습 서버에 정상 접속되었습니다.</p>
        </div>
    </body>
    </html>
    """

# API 확인용 JSON 엔드포인트
@app.get("/api/hello")
def api_hello():
    return {"message": "안녕하세요 조기훈입니다", "author": "조기훈"}

# 헬스체크 엔드포인트
@app.get("/health")
def health():
    return {"status": "ok"}
