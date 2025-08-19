"""
Posture Check App Backend - 메인 애플리케이션

이 파일은 FastAPI 애플리케이션의 진입점입니다.
- 애플리케이션 설정 및 초기화
- 미들웨어 구성 (CORS 등)
- API 라우터 등록
- 헬스 체크 및 시스템 엔드포인트
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import contextmanager
import pymysql
import os

# 설정 및 데이터베이스 모듈 import
from .core.config import settings
from .db.session import init_db, get_db
from .api.v1.routers import api_router

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="자세 교정 앱 백엔드 API",
    version=settings.VERSION
)

# CORS 미들웨어 설정 (Cross-Origin Resource Sharing)
# 프론트엔드와 백엔드 간 통신을 위한 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # 허용할 도메인 목록
    allow_credentials=True,  # 쿠키/인증 헤더 허용
    allow_methods=["*"],     # 모든 HTTP 메서드 허용
    allow_headers=["*"],     # 모든 헤더 허용
)

# API 라우터 등록
# v1 API의 모든 엔드포인트를 /api/v1 경로에 등록
app.include_router(api_router, prefix=settings.API_V1_STR)

# 데이터베이스 연결 설정 (기존 PyMySQL 연결 유지)
# Docker Compose 환경에서의 직접 연결을 위한 설정
DB_CONFIG = {
    'host': settings.DB_HOST,
    'port': settings.DB_PORT,
    'user': settings.DB_USER,
    'password': settings.DB_PASSWORD,
    'database': settings.DB_NAME,
    'charset': 'utf8mb4'
}

@contextmanager
def get_db_connection():
    """
    데이터베이스 연결을 관리하는 컨텍스트 매니저
    
    PyMySQL을 사용한 직접 데이터베이스 연결
    SQLAlchemy와 별도로 헬스 체크용으로 사용
    """
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        yield connection
    except Exception as e:
        print(f"데이터베이스 연결 오류: {e}")
        raise
    finally:
        if connection:
            connection.close()

@app.on_event("startup")
async def startup_event():
    """
    애플리케이션 시작 시 실행되는 이벤트 핸들러
    
    - 데이터베이스 테이블 자동 생성
    - 초기 설정 및 로그 출력
    """
    print("🚀 Posture Check App Backend 시작 중...")
    try:
        # SQLAlchemy를 사용한 데이터베이스 테이블 생성
        init_db()
        print("✅ 데이터베이스 테이블 생성 완료")
    except Exception as e:
        print(f"❌ 데이터베이스 초기화 실패: {e}")

@app.get("/")
def read_root():
    """
    루트 엔드포인트
    
    애플리케이션 기본 정보 및 사용 가능한 엔드포인트 안내
    """
    return {
        "message": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",      # Swagger UI 문서
        "health": "/health"   # 헬스 체크
    }

@app.get("/health")
def health_check():
    """
    헬스 체크 엔드포인트
    
    애플리케이션과 데이터베이스 연결 상태를 확인
    """
    try:
        # 데이터베이스 연결 테스트
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result[0] == 1:
                    return {
                        "status": "healthy",
                        "database": "connected",
                        "message": "애플리케이션이 정상적으로 작동 중입니다."
                    }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "message": "데이터베이스 연결에 문제가 있습니다."
        }
    
    return {
        "status": "unhealthy",
        "message": "알 수 없는 오류가 발생했습니다."
    }

# Render 배포를 위한 포트 설정
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
