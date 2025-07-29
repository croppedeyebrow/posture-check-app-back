"""
로컬 개발용 메인 파일
Docker와 병행 사용을 위한 별도 실행 파일
"""

import uvicorn
import sys
import os

# 로컬 설정을 사용하도록 환경 변수 설정
os.environ["USE_LOCAL_CONFIG"] = "true"

if __name__ == "__main__":
    print("🚀 로컬 개발 서버 시작...")
    print("🗄️ 로컬 MySQL 사용")
    print("🌐 포트: 8001")
    print("📚 API 문서: http://localhost:8001/docs")
    print("🏥 헬스 체크: http://localhost:8001/health")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,  # Docker와 다른 포트 사용
        reload=True,
        log_level="info"
    ) 