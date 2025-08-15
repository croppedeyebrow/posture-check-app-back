"""
사용자 관련 Pydantic 스키마

API 요청/응답에서 사용되는 사용자 데이터 검증 및 직렬화를 위한 스키마들
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """사용자 기본 정보 스키마 (공통 필드)"""
    # 사용자명 (3-50자, 로그인 ID로 사용)
    username: str = Field(..., min_length=3, max_length=50)
    # 이메일 주소 (회원가입/비밀번호 재설정용)
    email: EmailStr

class UserCreate(UserBase):
    """사용자 생성 스키마 (회원가입용)"""
    # 비밀번호 (최소 6자, API에서만 사용, DB에는 해시화되어 저장)
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    """사용자 정보 수정 스키마 (선택적 필드 업데이트)"""
    # 사용자명 (선택적 수정)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    # 이메일 주소 (선택적 수정)
    email: Optional[EmailStr] = None
    # 비밀번호 (선택적 수정, 최소 6자)
    password: Optional[str] = Field(None, min_length=6)

class User(UserBase):
    """사용자 응답 스키마 (API 응답용, 민감한 정보 제외)"""
    # 사용자 고유 식별자
    id: int
    # 계정 활성화 상태 (True: 활성화, False: 비활성화)
    is_active: bool
    # 계정 생성 시간
    created_at: datetime
    # 계정 정보 수정 시간
    updated_at: datetime
    
    class Config:
        # SQLAlchemy 모델에서 Pydantic 모델로 변환 허용
        from_attributes = True 