"""
Posture Check App Backend - 사용자 모델

이 모듈은 사용자 계정 정보를 관리하는 데이터베이스 모델을 정의합니다.
- 사용자 기본 정보 (이름, 이메일, 비밀번호 등)
- 계정 생성 및 수정 시간
- 계정 활성화 상태
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base

class User(Base):
    """
    사용자 모델
    
    사용자의 기본 정보와 인증 관련 데이터를 저장
    """
    __tablename__ = "users"
    
    # ==================== 기본 정보 ====================
    id = Column(Integer, primary_key=True, index=True, comment="사용자 고유 ID")
    email = Column(String(255), unique=True, index=True, nullable=False, comment="이메일 주소")
    username = Column(String(100), unique=True, index=True, nullable=False, comment="사용자명")
    full_name = Column(String(200), nullable=True, comment="전체 이름")
    
    # ==================== 인증 정보 ====================
    hashed_password = Column(String(255), nullable=False, comment="해시된 비밀번호")
    
    # ==================== 계정 상태 ====================
    is_active = Column(Boolean, default=True, comment="계정 활성화 상태")
    is_verified = Column(Boolean, default=False, comment="이메일 인증 상태")
    
    # ==================== 추가 정보 ====================
    profile_image = Column(Text, nullable=True, comment="프로필 이미지 URL")
    bio = Column(Text, nullable=True, comment="자기소개")
    
    # ==================== 시간 정보 ====================
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="계정 생성 시간")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="정보 수정 시간")
    last_login = Column(DateTime(timezone=True), nullable=True, comment="마지막 로그인 시간")
    
    # ==================== 관계 설정 ====================
    posture_sessions = relationship("PostureSession", back_populates="user")
    posture_records = relationship("PostureRecord", back_populates="user")
    posture_analyses = relationship("PostureAnalysis", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>" 