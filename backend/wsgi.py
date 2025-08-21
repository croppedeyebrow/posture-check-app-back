#!/usr/bin/env python3
"""
WSGI 애플리케이션 진입점
Render 배포용
"""

import os
import sys

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 배포 환경 설정
os.environ["USE_LOCAL_CONFIG"] = "false"

# FastAPI 앱 import
from app.main import app

# WSGI 애플리케이션
application = app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
