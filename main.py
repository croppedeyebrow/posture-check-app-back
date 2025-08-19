#!/usr/bin/env python3
"""
Posture Check App Backend - 메인 실행 파일

Render 배포를 위한 진입점
"""

import uvicorn
import os
import sys

# backend 디렉토리를 Python 경로에 추가
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

# FastAPI 앱 import
from app.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
