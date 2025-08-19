"""
Posture Check App Backend - 데이터베이스 베이스 모듈

이 모듈은 모든 데이터베이스 모델의 베이스 클래스를 정의합니다.
"""

# Import all the models, so that Base has them before being imported by Alembic
from .session import Base
from ..models import user, posture

# 모든 모델을 여기서 import하여 Alembic이 인식할 수 있도록 함
__all__ = ["Base", "user", "posture"] 