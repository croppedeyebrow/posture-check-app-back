from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Posture Record 관련 스키마 (프론트엔드 13개 필드 반영)
class PostureRecordBase(BaseModel):
    # 기존 7개 필드
    neck_angle: float = Field(..., description="목 각도")
    shoulder_slope: float = Field(..., description="어깨 기울기")
    head_forward: float = Field(..., description="머리 전방 이동")
    shoulder_height_diff: float = Field(..., description="어깨 높이 차이")
    score: float = Field(..., description="종합 점수")
    
    # 신규 추가 6개 필드
    cervical_lordosis: float = Field(..., description="경추 전만각")
    forward_head_distance: float = Field(..., description="전방 머리 거리 (mm)")
    head_tilt: float = Field(..., description="머리 측면 기울기")
    left_shoulder_height_diff: float = Field(..., description="왼쪽 어깨 높이 차이")
    left_scapular_winging: float = Field(..., description="왼쪽 견갑골 날개")
    right_scapular_winging: float = Field(..., description="오른쪽 견갑골 날개")
    shoulder_forward_movement: float = Field(..., description="어깨 전방 이동")
    
    # 메타데이터
    session_id: str = Field(..., description="세션 ID")
    device_info: Optional[str] = Field(None, description="기기 정보")

class PostureRecordCreate(PostureRecordBase):
    pass

class PostureRecord(PostureRecordBase):
    id: int
    user_id: int
    is_neck_angle_normal: Optional[bool] = None
    is_forward_head_normal: Optional[bool] = None
    is_head_tilt_normal: Optional[bool] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Posture Session 관련 스키마
class PostureSessionBase(BaseModel):
    session_id: str
    device_info: Optional[str] = None

class PostureSessionCreate(PostureSessionBase):
    pass

class PostureSession(PostureSessionBase):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    total_records: int
    average_score: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Posture Analysis 관련 스키마
class PostureAnalysisBase(BaseModel):
    problem_description: str
    solution_suggestion: str
    severity_level: str = Field(..., regex="^(low|medium|high)$")
    neck_angle_deviation: float
    forward_head_deviation: float
    head_tilt_deviation: float

class PostureAnalysisCreate(PostureAnalysisBase):
    session_id: str

class PostureAnalysis(PostureAnalysisBase):
    id: int
    user_id: int
    session_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# API 응답 스키마
class HealthCheck(BaseModel):
    status: str
    database: str
    message: str

class PostureStats(BaseModel):
    total_records: int
    average_score: float
    improvement_rate: float
    normal_posture_rate: float
    last_measurement: Optional[datetime] = None

class PostureTrend(BaseModel):
    date: str
    average_score: float
    record_count: int
    neck_angle_avg: float
    forward_head_distance_avg: float

# 의학적 기준 상수
class MedicalStandards(BaseModel):
    neck_angle_normal_range: tuple = (-30, 30)  # 목 각도 정상 범위 (도)
    forward_head_normal_max: float = 100.0  # 전방 머리 거리 최대 정상값 (mm)
    head_tilt_normal_range: tuple = (-15, 15)  # 머리 기울기 정상 범위 (도) 