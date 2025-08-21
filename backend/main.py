#!/usr/bin/env python3
"""
Posture Check App Backend - 메인 실행 파일

로컬 개발 및 배포 통합 진입점
"""

import uvicorn
import os
import sys

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 로컬 개발 환경에서는 로컬 설정 사용
if not os.environ.get("RENDER") and not os.environ.get("RAILWAY"):
    os.environ["USE_LOCAL_CONFIG"] = "true"
    print("🔧 로컬 환경 감지: USE_LOCAL_CONFIG=true 설정")
else:
    print("🔧 배포 환경 감지: USE_LOCAL_CONFIG=false 설정")

# FastAPI 앱 import
from app.main import app

if __name__ == "__main__":
    # 환경에 따른 포트 설정
    if os.environ.get("USE_LOCAL_CONFIG"):
        port = 8000
        print("🚀 로컬 개발 서버 시작...")
        print("🗄️ 로컬 MySQL 사용")
        print("🌐 포트: 8000")
        print("📚 API 문서: http://localhost:8000/docs")
        print("🏥 헬스 체크: http://localhost:8000/health")
        reload = True
        log_level = "debug"
    else:
        port = int(os.environ.get("PORT", 8000))
        reload = False
        log_level = "info"
    
    if reload:
        # reload 모드에서는 import string 사용
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0", 
            port=port, 
            reload=True,
            log_level=log_level
        )
    else:
        # 배포 모드에서는 직접 app 객체 사용
        uvicorn.run(
            app,
            host="0.0.0.0", 
            port=port, 
            reload=False,
            log_level=log_level
        )
