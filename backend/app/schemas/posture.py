from pydantic import BaseModel, Field, validator
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
    
    # 프론트엔드 추가 필드
    head_rotation: float = Field(..., description="머리 회전")
    issues: Optional[str] = Field(default="[]", description="발견된 문제점들 (JSON 문자열)")
    
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
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 프론트엔드 요구사항에 맞는 새로운 스키마 (camelCase 필드명 사용)
class PostureDataSave(BaseModel):
    userId: int = Field(..., description="사용자 ID")
    score: float = Field(..., ge=0, le=100, description="자세 점수 (0-100)")
    neckAngle: float = Field(..., description="목 각도")
    shoulderSlope: float = Field(..., description="어깨 기울기")
    headForward: float = Field(..., description="머리 전방 돌출도")
    shoulderHeightDiff: float = Field(..., description="어깨 높이 차이")
    cervicalLordosis: Optional[float] = Field(0.0, description="경추 전만")
    forwardHeadDistance: float = Field(..., description="머리 전방 이동 거리")
    headTilt: float = Field(..., description="머리 기울기")
    headRotation: Optional[float] = Field(0.0, description="머리 회전")
    shoulderForwardMovement: Optional[float] = Field(0.0, description="어깨 전방 이동")
    issues: Optional[List[dict]] = Field(default=[], description="발견된 문제점들")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="측정 시간")
    sessionId: Optional[str] = Field(None, description="세션 ID")
    deviceInfo: Optional[str] = Field(None, description="기기 정보")
    
    # 문자열을 숫자로 자동 변환하는 validator 추가
    
    @validator('neckAngle', 'shoulderSlope', 'headForward', 'shoulderHeightDiff', 
               'cervicalLordosis', 'forwardHeadDistance', 'headTilt', 'headRotation', 
               'shoulderForwardMovement', pre=True)
    def convert_string_to_float(cls, v):
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                return 0.0
        return v
    
    @validator('score', pre=True)
    def convert_score_to_float(cls, v):
        if isinstance(v, (str, int)):
            try:
                return float(v)
            except ValueError:
                return 0.0
        return v
    
    @validator('userId', pre=True)
    def convert_user_id_to_int(cls, v):
        if isinstance(v, str):
            try:
                return int(v)
            except ValueError:
                return 1
        return v


class PostureAnalysisConfig(BaseModel):
    user_id: int = Field(..., description="사용자 ID")
    session_id: Optional[str] = Field(None, description="세션 ID")
    device_info: Optional[str] = Field(None, description="기기 정보")
    analysis_interval: Optional[int] = Field(5, description="분석 간격 (초)")

class PostureAnalysisSession(BaseModel):
    session_id: str
    user_id: int
    start_time: datetime
    status: str = "active"  # active, stopped
    device_info: Optional[str] = None

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
    severity_level: str = Field(..., pattern="^(low|medium|high)$")
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