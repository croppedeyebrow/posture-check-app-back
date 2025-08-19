#!/usr/bin/env python3
"""
Posture Check App Backend - 메인 실행 파일

Render 배포를 위한 진입점
"""

import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # 현재 디렉토리를 Python 경로에 추가하고 app.main:app 실행
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
