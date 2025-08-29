from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
from pydantic import BaseModel

from ....db.session import get_db
from ....schemas.user import UserCreate, User, UserUpdate
from ....crud.user import user as user_crud
from ....core.security import create_access_token, get_current_user, get_password_hash
from ....core.config import settings

router = APIRouter()

# 로그인 스키마
class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str

@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """사용자 로그인"""
    try:
        # 사용자 인증 (이메일로 사용자 찾기)
        user = user_crud.authenticate_by_email(db, email=user_credentials.email, password=user_credentials.password)
        if not user:
            raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비밀번호입니다")
        
        if not user_crud.is_active(user):
            raise HTTPException(status_code=400, detail="비활성화된 사용자입니다")
        
        # 액세스 토큰 생성
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            subject=user.username, expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"로그인 실패: {str(e)}")

@router.post("/register", response_model=User)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """새 사용자 등록"""
    try:
        print(f"🔍 회원가입 시도: username={user_in.username}, email={user_in.email}")
        
        # 이메일 중복 확인
        existing_user = user_crud.get_by_email(db, email=user_in.email)
        if existing_user:
            print(f"❌ 이메일 중복: {user_in.email}")
            raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")
        
        # 사용자명 중복 확인
        existing_username = user_crud.get_by_username(db, username=user_in.username)
        if existing_username:
            print(f"❌ 사용자명 중복: {user_in.username}")
            raise HTTPException(status_code=400, detail="이미 사용 중인 사용자명입니다")
        
        print(f"✅ 중복 확인 완료, 사용자 생성 중...")
        user = user_crud.create(db, obj_in=user_in)
        print(f"✅ 사용자 생성 완료: ID={user.id}")
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 회원가입 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"사용자 등록 실패: {str(e)}")

@router.get("/me", response_model=User)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """현재 로그인한 사용자 정보 조회"""
    return current_user

@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """사용자 ID로 사용자 정보 조회"""
    try:
        user = user_crud.get(db, id=user_id)
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사용자 조회 실패: {str(e)}")

@router.put("/me", response_model=User)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 사용자 정보 업데이트"""
    try:
        # 이메일 변경 시 중복 확인
        if user_update.email and user_update.email != current_user.email:
            existing_user = user_crud.get_by_email(db, email=user_update.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다")
        
        # 사용자명 변경 시 중복 확인
        if user_update.username and user_update.username != current_user.username:
            existing_username = user_crud.get_by_username(db, username=user_update.username)
            if existing_username:
                raise HTTPException(status_code=400, detail="이미 사용 중인 사용자명입니다")
        
        user = user_crud.update(db, db_obj=current_user, obj_in=user_update)
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사용자 정보 업데이트 실패: {str(e)}")

@router.get("/", response_model=List[User])
def get_users(
    skip: int = Query(0, description="건너뛸 레코드 수"),
    limit: int = Query(100, description="조회할 레코드 수"),
    db: Session = Depends(get_db)
):
    """사용자 목록 조회 (관리자용)"""
    try:
        users = db.query(user_crud.model).offset(skip).limit(limit).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사용자 목록 조회 실패: {str(e)}")

@router.delete("/me")
def delete_current_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 사용자 계정 삭제"""
    try:
        db.delete(current_user)
        db.commit()
        return {"message": "사용자 계정이 성공적으로 삭제되었습니다"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사용자 계정 삭제 실패: {str(e)}")
