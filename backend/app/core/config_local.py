"""
로컬 개발용 설정 파일
로컬 MySQL과 Docker MySQL 분리 사용
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
from dotenv import load_dotenv

# .env.local 파일에서 환경 변수 로드 (있는 경우)
load_dotenv(".env.local")

class LocalSettings(BaseSettings):
    """
    로컬 개발용 설정 클래스
    로컬 MySQL에 연결하도록 설정
    """
    
    # ==================== API 설정 ====================
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Posture Check App Backend (Local)"
    VERSION: str = "1.0.0-local"
    
    # ==================== 데이터베이스 설정 (로컬 MySQL 사용) ====================
    DB_HOST: str = "localhost"  # 로컬 MySQL
    DB_PORT: int = 3306         # 로컬 MySQL 기본 포트
    DB_USER: str = "root"
    DB_PASSWORD: str = "Lee289473007216!"       # 로컬 MySQL 비밀번호 (설정에 따라 변경)
    DB_NAME: str = "posture_app_local"  # 로컬용 별도 데이터베이스
    
    # ==================== 보안 설정 ====================
    SECRET_KEY: str = "posture-app-secret-key-2024-local"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ==================== CORS 설정 ====================
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # ==================== 의학적 기준 설정 ====================
    NECK_ANGLE_NORMAL_MIN: float = -30.0
    NECK_ANGLE_NORMAL_MAX: float = 30.0
    FORWARD_HEAD_DISTANCE_MAX: float = 100.0
    HEAD_TILT_NORMAL_MIN: float = -15.0
    HEAD_TILT_NORMAL_MAX: float = 15.0
    
    class Config:
        case_sensitive = True
        env_file = ".env.local"

# 로컬 설정 인스턴스
local_settings = LocalSettings() 