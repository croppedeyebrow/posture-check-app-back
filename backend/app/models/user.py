from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..db.base import Base

class User(Base):
    """사용자 테이블"""
    __tablename__ = "users"
    
    # 사용자 고유 식별자 (자동 증가)
    id = Column(Integer, primary_key=True, index=True)
    
    # 사용자명 (로그인 ID로 사용, 중복 불가)
    username = Column(String(50), unique=True, index=True, nullable=False)
    
    # 이메일 주소 (회원가입/비밀번호 재설정용, 중복 불가)
    email = Column(String(100), unique=True, index=True, nullable=False)
    
    # 해시화된 비밀번호 (보안을 위해 원본 비밀번호는 저장하지 않음)
    hashed_password = Column(String(255), nullable=False)
    
    # 계정 활성화 상태 (True: 활성화, False: 비활성화/정지)
    is_active = Column(Boolean, default=True)
    
    # 계정 생성 시간 (자동 설정)
    created_at = Column(DateTime, default=func.now())
    
    # 계정 정보 수정 시간 (자동 업데이트)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now()) 