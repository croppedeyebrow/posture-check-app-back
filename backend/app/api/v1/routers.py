from fastapi import APIRouter
from .endpoints import posture, user

# v1 API 라우터 생성
api_router = APIRouter()

# 자세 관련 라우터 등록
api_router.include_router(
    posture.router,
    prefix="/posture",
    tags=["posture"]
)

# 사용자 관련 라우터 등록
api_router.include_router(
    user.router,
    prefix="/users",
    tags=["users"]
) 