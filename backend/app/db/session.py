"""
Posture Check App Backend - 데이터베이스 세션 관리

이 모듈은 SQLAlchemy를 사용한 데이터베이스 연결과 세션을 관리합니다.
- 데이터베이스 엔진 생성 및 설정
- 세션 팩토리 생성
- 의존성 주입을 위한 세션 제공 함수
- 데이터베이스 초기화 함수
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings

# ==================== 데이터베이스 URL 구성 ====================
# MySQL + PyMySQL 드라이버를 사용한 연결 문자열 생성
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# ==================== SQLAlchemy 엔진 생성 ====================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 연결 상태 확인 (연결이 끊어진 경우 자동 재연결)
    pool_recycle=3600,   # 1시간마다 연결 재생성 (MySQL 연결 타임아웃 방지)
    echo=False           # SQL 로그 출력 여부 (개발 시 True로 설정 가능)
)

# ==================== 세션 팩토리 생성 ====================
# 데이터베이스 세션을 생성하는 팩토리
# autocommit=False: 트랜잭션 수동 관리
# autoflush=False: 자동 플러시 비활성화
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ==================== 데이터베이스 의존성 함수 ====================
def get_db():
    """
    데이터베이스 세션을 제공하는 의존성 함수
    
    FastAPI의 Depends에서 사용되어 각 요청마다 새로운 데이터베이스 세션을 제공
    요청이 완료되면 자동으로 세션을 닫음
    
    Returns:
        Session: SQLAlchemy 데이터베이스 세션
    """
    db = SessionLocal()
    try:
        yield db  # 세션을 요청 처리 함수에 제공
    finally:
        db.close()  # 요청 완료 후 세션 닫기

# ==================== 데이터베이스 초기화 함수 ====================
def init_db():
    """
    데이터베이스 테이블 생성
    
    애플리케이션 시작 시 모든 모델의 테이블을 자동으로 생성
    기존 테이블이 있는 경우 무시됨
    """
    from ..db.base import Base
    # 모든 모델들을 import하여 테이블 생성
    from ..models.user import User
    from ..models.posture import PostureRecord, PostureSession, PostureAnalysis
    Base.metadata.create_all(bind=engine) 