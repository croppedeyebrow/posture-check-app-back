from fastapi import APIRouter
from .endpoints import posture

# v1 API 라우터 생성
api_router = APIRouter()

# 자세 관련 라우터 등록
api_router.include_router(
    posture.router,
    prefix="/posture",
    tags=["posture"]
) 