"""
Posture Check App Backend - 데이터베이스 세션 관리 모듈

이 모듈은 SQLAlchemy를 사용한 데이터베이스 연결 및 세션 관리를 담당합니다.
- 데이터베이스 엔진 생성
- 세션 팩토리 설정
- 연결 풀 관리
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..core.config import settings
import os

# 데이터베이스 URL 구성
DATABASE_URL = settings.get_database_url()

# Railway MySQL 연결 설정
def get_connect_args():
    """데이터베이스 연결 인자 반환"""
    # Railway는 기본적으로 SSL을 지원하므로 별도 설정 불필요
    return {}

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 연결 상태 확인
    pool_recycle=300,    # 5분마다 연결 재생성
    pool_size=10,        # 연결 풀 크기
    max_overflow=20,     # 최대 오버플로우 연결 수
    echo=False,          # SQL 로그 출력 (개발 시 True로 설정)
    connect_args=get_connect_args()
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 클래스 생성
Base = declarative_base()

def get_db():
    """
    데이터베이스 세션 생성기
    
    각 요청마다 새로운 세션을 생성하고 요청 완료 후 자동으로 닫힘
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    데이터베이스 초기화
    
    모든 테이블을 생성합니다.
    """
    # 모든 모델을 import하여 테이블 생성
    from ..models import user, posture
    
    Base.metadata.create_all(bind=engine) 