"""app 패키지 진입점. 실행: python -m uvicorn app.main:app --reload"""
import sys
from pathlib import Path

# 상위 폴더(08_daily_project)를 sys.path에 추가하여 storage 모듈 공유
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# main.py의 app 인스턴스를 재노출
from main import app  # noqa: F401
