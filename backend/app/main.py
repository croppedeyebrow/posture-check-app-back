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
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # 허용할 도메인 목록
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
    
    애플리케이션과 데이터베이스의 상태를 확인
    로드 밸런서나 모니터링 시스템에서 사용
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return {
                    "status": "healthy",
                    "database": "connected",
                    "message": "자세 교정 앱 백엔드가 정상적으로 작동 중입니다.",
                    "version": settings.VERSION
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터베이스 연결 실패: {str(e)}")

@app.get("/db-test")
def test_database():
    """
    데이터베이스 테스트 엔드포인트
    
    개발 및 디버깅용 엔드포인트
    데이터베이스 연결 및 기본 CRUD 작업 테스트
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # 테스트 테이블 생성 (없는 경우)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS test_table (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        message VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # 테스트 데이터 삽입
                cursor.execute("INSERT INTO test_table (message) VALUES (%s)", ("Posture Check App 테스트",))
                conn.commit()
                
                # 데이터 조회
                cursor.execute("SELECT * FROM test_table ORDER BY created_at DESC LIMIT 5")
                results = cursor.fetchall()
                
                return {
                    "message": "데이터베이스 테스트 성공",
                    "data": [
                        {"id": row[0], "message": row[1], "created_at": str(row[2])}
                        for row in results
                    ]
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터베이스 테스트 실패: {str(e)}")

@app.get("/api-info")
def get_api_info():
    """
    API 정보 조회 엔드포인트
    
    애플리케이션의 기능과 사용 가능한 엔드포인트 정보 제공
    개발자 문서화 및 API 탐색용
    """
    return {
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": "자세 교정 앱을 위한 FastAPI 백엔드",
        "features": [
            "자세 기록 저장 및 조회",
            "실시간 자세 분석",
            "의학적 기준 기반 판단",
            "자세 통계 및 트렌드 분석",
            "13개 자세 지표 지원"
        ],
        "endpoints": {
            "posture": f"{settings.API_V1_STR}/posture/*",  # 자세 관련 API
            "health": "/health",                            # 헬스 체크
            "docs": "/docs"                                 # API 문서
        }
    }
