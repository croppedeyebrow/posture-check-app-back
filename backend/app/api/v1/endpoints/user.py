from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
from pydantic import BaseModel

from ....db.session import get_db
from ....schemas.user import UserCreate, User, UserUpdate
from ....crud.user import user as user_crud
from ....core.security import create_access_token, get_current_user, get_password_hash, verify_password, create_password_reset_token, verify_password_reset_token
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

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetResponse(BaseModel):
    email: str
    message: str
    reset_token: str

class PasswordResetConfirm(BaseModel):
    email: str
    reset_token: str
    new_password: str

class PasswordResetConfirmResponse(BaseModel):
    email: str
    message: str

@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """사용자 로그인"""
    try:
        print(f"🔍 로그인 시도: email={user_credentials.email}")
        
        # 사용자 인증 (이메일로 사용자 찾기)
        user = user_crud.authenticate_by_email(db, email=user_credentials.email, password=user_credentials.password)
        if not user:
            print(f"❌ 로그인 실패: 잘못된 이메일 또는 비밀번호 - {user_credentials.email}")
            raise HTTPException(status_code=401, detail="잘못된 이메일 또는 비밀번호입니다")
        
        if not user_crud.is_active(user):
            print(f"❌ 로그인 실패: 비활성화된 사용자 - {user_credentials.email}")
            raise HTTPException(status_code=400, detail="비활성화된 사용자입니다")
        
        print(f"✅ 로그인 성공: username={user.username}, user_id={user.id}")
        
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
        print(f"❌ 로그인 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"로그인 실패: {str(e)}")

@router.post("/forgot-password", response_model=PasswordResetResponse)
def forgot_password(
    password_reset: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """비밀번호 찾기 - 재설정 토큰 생성"""
    try:
        print(f"🔍 비밀번호 찾기 요청: email={password_reset.email}")
        
        # 이메일로 사용자 찾기
        user = user_crud.get_by_email(db, email=password_reset.email)
        if not user:
            print(f"❌ 사용자를 찾을 수 없음: {password_reset.email}")
            # 보안상 사용자가 존재하지 않아도 같은 메시지 반환
            return PasswordResetResponse(
                email=password_reset.email,
                message="비밀번호 재설정 링크가 이메일로 전송되었습니다. (존재하지 않는 이메일인 경우 무시하세요)",
                reset_token=""
            )
        
        print(f"✅ 사용자 발견: username={user.username}, user_id={user.id}")
        
        # 비밀번호 재설정 토큰 생성 (1시간 유효)
        reset_token = create_password_reset_token(email=password_reset.email)
        
        print(f"✅ 비밀번호 재설정 토큰 생성: {reset_token[:20]}...")
        
        # 실제 프로덕션에서는 여기서 이메일 발송 로직 추가
        # send_password_reset_email(user.email, reset_token)
        
        return PasswordResetResponse(
            email=password_reset.email,
            message="비밀번호 재설정 링크가 이메일로 전송되었습니다. (개발환경에서는 토큰을 직접 확인하세요)",
            reset_token=reset_token  # 개발환경에서만 토큰 반환
        )
        
    except Exception as e:
        print(f"❌ 비밀번호 찾기 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"비밀번호 찾기 실패: {str(e)}")

@router.post("/reset-password", response_model=PasswordResetConfirmResponse)
def reset_password(
    password_reset: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """비밀번호 재설정"""
    try:
        print(f"🔍 비밀번호 재설정 시도: email={password_reset.email}")
        
        # 토큰 검증
        email_from_token = verify_password_reset_token(password_reset.reset_token)
        if not email_from_token or email_from_token != password_reset.email:
            print(f"❌ 유효하지 않은 토큰: {password_reset.email}")
            raise HTTPException(status_code=400, detail="유효하지 않은 재설정 토큰입니다")
        
        # 사용자 찾기
        user = user_crud.get_by_email(db, email=password_reset.email)
        if not user:
            print(f"❌ 사용자를 찾을 수 없음: {password_reset.email}")
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        
        print(f"✅ 사용자 발견: username={user.username}, user_id={user.id}")
        
        # 새 비밀번호로 업데이트
        user_update = UserUpdate(password=password_reset.new_password)
        updated_user = user_crud.update(db, db_obj=user, obj_in=user_update)
        
        print(f"✅ 비밀번호 재설정 완료: {password_reset.email}")
        
        return PasswordResetConfirmResponse(
            email=password_reset.email,
            message="비밀번호가 성공적으로 재설정되었습니다"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 비밀번호 재설정 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"비밀번호 재설정 실패: {str(e)}")

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
