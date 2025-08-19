"""
Posture Check App Backend - 설정 관리 모듈

이 모듈은 애플리케이션의 모든 설정을 중앙에서 관리합니다.
- 환경 변수 로드 및 검증
- 데이터베이스 연결 설정
- 보안 설정
- API 설정
- 의학적 기준 설정
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스
    
    Pydantic BaseSettings를 상속하여 환경 변수 자동 로드 및 검증
    """
    
    # ==================== API 설정 ====================
    API_V1_STR: str = "/api/v1"                    # API 버전 경로
    PROJECT_NAME: str = "Posture Check App Backend" # 프로젝트 이름
    VERSION: str = "1.0.0"                         # 애플리케이션 버전
    
    # ==================== 데이터베이스 설정 ====================
    DB_HOST: str = os.getenv("DB_HOST", "localhost")           # 데이터베이스 호스트
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))           # 데이터베이스 포트
    DB_USER: str = os.getenv("DB_USER", "user")               # 데이터베이스 사용자
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")    # 데이터베이스 비밀번호
    DB_NAME: str = os.getenv("DB_NAME", "testdb")             # 데이터베이스 이름
    
    # 배포용 데이터베이스 연결 URL (우선순위: DATABASE_URL > MYSQL_PUBLIC_URL > 개별 설정)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    MYSQL_PUBLIC_URL: Optional[str] = os.getenv("MYSQL_PUBLIC_URL")
    
    # ==================== 보안 설정 ====================
    SECRET_KEY: str = os.getenv("SECRET_KEY", "posture-app-secret-key-2024")  # JWT 시크릿 키
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")                          # JWT 알고리즘
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # 토큰 만료 시간
    
    # ==================== CORS 설정 ====================
    BACKEND_CORS_ORIGINS: List[str] = [
        "https://posture-check-app.vercel.app",  # Vercel 프론트엔드
        "http://localhost:3000",                 # 로컬 개발용
        "http://localhost:8080",                 # 로컬 개발용
        "*"                                      # 개발용 (모든 도메인 허용)
    ]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # ==================== 의학적 기준 설정 ====================
    # 실제 의료 기준을 반영한 자세 판단 기준값들
    NECK_ANGLE_NORMAL_MIN: float = -30.0    # 목 각도 정상 범위 최소값 (도)
    NECK_ANGLE_NORMAL_MAX: float = 30.0     # 목 각도 정상 범위 최대값 (도)
    FORWARD_HEAD_DISTANCE_MAX: float = 100.0 # 전방 머리 거리 최대 정상값 (mm)
    HEAD_TILT_NORMAL_MIN: float = -15.0     # 머리 기울기 정상 범위 최소값 (도)
    HEAD_TILT_NORMAL_MAX: float = 15.0      # 머리 기울기 정상 범위 최대값 (도)
    
    def get_database_url(self) -> str:
        """
        데이터베이스 연결 URL 반환
        
        우선순위: DATABASE_URL > MYSQL_PUBLIC_URL > 개별 설정으로 구성
        """
        # 1. DATABASE_URL 우선 사용 (Render 배포용)
        if self.DATABASE_URL:
            return self.DATABASE_URL
        
        # 2. MYSQL_PUBLIC_URL 사용 (Railway 직접 연결용)
        if self.MYSQL_PUBLIC_URL:
            return self.MYSQL_PUBLIC_URL
        
        # 3. 개별 설정으로 구성 (로컬 개발용)
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        """
        Pydantic 설정
        
        case_sensitive: 대소문자 구분
        env_file: 환경 변수 파일 경로
        """
        case_sensitive = True
        env_file = ".env"

# 전역 설정 인스턴스 생성
# 애플리케이션 전체에서 이 인스턴스를 사용하여 설정에 접근
import os

# 로컬 설정 사용 여부 확인
if os.getenv("USE_LOCAL_CONFIG") == "true":
    from .config_local import local_settings
    settings = local_settings
else:
    settings = Settings() 