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
    allow_origins=[
        # 프로덕션 도메인
        "https://posture-check-app.vercel.app",
        "https://posture-check-app-git-main-croppedeyebrow.vercel.app",
        
        # 개발 환경
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        
        # Vercel 프리뷰 도메인 (필요한 경우)
        "https://posture-check-app-*.vercel.app",
        
        # 개발 중 임시 허용 (나중에 제거)
        "http://localhost:8080",
        "http://localhost:8000"
    ],
    allow_credentials=True,  # 쿠키/인증 헤더 허용
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],  # 허용할 HTTP 메서드
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers"
    ],
    expose_headers=["*"],  # 응답 헤더 노출
    max_age=86400,  # CORS 프리플라이트 캐시 시간 (24시간)
)

# API 라우터 등록
# v1 API의 모든 엔드포인트를 /api/v1 경로에 등록
app.include_router(api_router, prefix=settings.API_V1_STR)

# 데이터베이스 연결 설정 (Render 환경 대응)
def get_db_config():
    """
    환경에 따른 데이터베이스 설정 반환
    Render 환경에서는 DATABASE_URL 또는 MYSQL_PUBLIC_URL 사용
    """
    # Render 환경에서 DATABASE_URL이 있는 경우
    if settings.DATABASE_URL:
        # mysql://user:pass@host:port/db 형식에서 파싱
        import re
        pattern = r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)'
        match = re.match(pattern, settings.DATABASE_URL)
        if match:
            user, password, host, port, database = match.groups()
            return {
                'host': host,
                'port': int(port),
                'user': user,
                'password': password,
                'database': database,
                'charset': 'utf8mb4'
            }
    
    # MYSQL_PUBLIC_URL이 있는 경우
    if settings.MYSQL_PUBLIC_URL:
        import re
        pattern = r'mysql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)'
        match = re.match(pattern, settings.MYSQL_PUBLIC_URL)
        if match:
            user, password, host, port, database = match.groups()
            return {
                'host': host,
                'port': int(port),
                'user': user,
                'password': password,
                'database': database,
                'charset': 'utf8mb4'
            }
    
    # 기본 설정 (로컬 개발용)
    return {
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
        db_config = get_db_config()
        print(f"데이터베이스 연결 시도: {db_config['host']}:{db_config['port']}")
        connection = pymysql.connect(**db_config)
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
    
    # 데이터베이스 설정 정보 출력
    db_config = get_db_config()
    print(f"📊 데이터베이스 설정: {db_config['host']}:{db_config['port']}")
    
    try:
        # SQLAlchemy를 사용한 데이터베이스 테이블 생성
        init_db()
        print("✅ 데이터베이스 테이블 생성 완료")
    except Exception as e:
        print(f"❌ 데이터베이스 초기화 실패: {e}")
        print("💡 환경 변수 설정을 확인해주세요:")
        print("   - DATABASE_URL 또는 MYSQL_PUBLIC_URL 설정")
        print("   - 또는 DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME 설정")

@app.get("/")
@app.head("/")
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
@app.head("/health")
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
                    db_config = get_db_config()
                    return {
                        "status": "healthy",
                        "database": "connected",
                        "database_host": db_config['host'],
                        "database_port": db_config['port'],
                        "message": "애플리케이션이 정상적으로 작동 중입니다."
                    }
    except Exception as e:
        db_config = get_db_config()
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "database_host": db_config['host'],
            "database_port": db_config['port'],
            "error": str(e),
            "message": "데이터베이스 연결에 문제가 있습니다."
        }
    
    return {
        "status": "unhealthy",
        "message": "알 수 없는 오류가 발생했습니다."
    }

@app.get("/api/test")
def api_test():
    """
    API 연결 테스트 엔드포인트
    
    프론트엔드에서 API 연결을 테스트하기 위한 간단한 엔드포인트
    """
    return {
        "message": "API 연결 성공!",
        "timestamp": "2024-08-20T05:15:00Z",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "api_v1": "/api/v1",
            "users": "/api/v1/users",
            "posture": "/api/v1/posture"
        }
    }

@app.get("/api/cors-test")
def cors_test():
    """
    CORS 테스트 엔드포인트
    
    CORS 설정이 올바르게 작동하는지 확인하기 위한 엔드포인트
    """
    return {
        "message": "CORS 테스트 성공!",
        "cors_enabled": True,
        "allowed_origins": [
            "https://posture-check-app.vercel.app",
            "https://posture-check-app-git-main-croppedeyebrow.vercel.app",
            "http://localhost:3000",
            "http://localhost:5173"
        ],
        "timestamp": "2024-08-20T06:10:00Z"
    }

@app.options("/api/cors-test")
def cors_test_options():
    """
    CORS 프리플라이트 요청 처리
    
    브라우저의 CORS 프리플라이트 요청에 대한 응답
    """
    return {"message": "CORS preflight successful"}

# Render 배포를 위한 포트 설정
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
