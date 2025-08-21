"""
Posture Check App Backend - 자세 모델

이 모듈은 자세 측정 및 분석과 관련된 데이터베이스 모델들을 정의합니다.
- PostureRecord: 개별 자세 측정 기록 (13개 지표)
- PostureSession: 자세 측정 세션 관리
- PostureAnalysis: 자세 분석 결과 및 통계
"""

from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base

class PostureSession(Base):
    """
    자세 측정 세션 모델
    
    자세 측정 세션의 기본 정보를 관리
    """
    __tablename__ = "posture_sessions"
    
    id = Column(Integer, primary_key=True, index=True, comment="세션 고유 ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    session_name = Column(String(200), nullable=True, comment="세션 이름")
    start_time = Column(DateTime(timezone=True), server_default=func.now(), comment="세션 시작 시간")
    end_time = Column(DateTime(timezone=True), nullable=True, comment="세션 종료 시간")
    is_active = Column(Boolean, default=True, comment="세션 활성화 상태")
    
    # 관계 설정
    user = relationship("User", back_populates="posture_sessions")
    
    def __repr__(self):
        return f"<PostureSession(id={self.id}, user_id={self.user_id}, name='{self.session_name}')>"

class PostureRecord(Base):
    """
    자세 측정 기록 모델
    
    프론트엔드에서 전송하는 13개 자세 지표 데이터를 저장
    """
    __tablename__ = "posture_records"
    
    id = Column(Integer, primary_key=True, index=True, comment="기록 고유 ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    
    # ==================== 프론트엔드 자세 지표 (13개) ====================
    # 1. 목 각도 (Neck Angle)
    neck_angle = Column(Float, nullable=True, comment="목 각도 (도)")
    
    # 2. 어깨 기울기 (Shoulder Slope)
    shoulder_slope = Column(Float, nullable=True, comment="어깨 기울기 (도)")
    
    # 3. 머리 전방 이동 (Head Forward)
    head_forward = Column(Float, nullable=True, comment="머리 전방 이동 (도)")
    
    # 4. 어깨 높이 차이 (Shoulder Height Difference)
    shoulder_height_diff = Column(Float, nullable=True, comment="어깨 높이 차이 (mm)")
    
    # 5. 종합 점수 (Score)
    score = Column(Float, nullable=True, comment="종합 자세 점수 (0-100)")
    
    # 6. 경추 전만각 (Cervical Lordosis)
    cervical_lordosis = Column(Float, nullable=True, comment="경추 전만각 (도)")
    
    # 7. 전방 머리 거리 (Forward Head Distance)
    forward_head_distance = Column(Float, nullable=True, comment="전방 머리 거리 (mm)")
    
    # 8. 머리 기울기 (Head Tilt)
    head_tilt = Column(Float, nullable=True, comment="머리 기울기 (도)")
    
    # 9. 왼쪽 어깨 높이 차이 (Left Shoulder Height Difference)
    left_shoulder_height_diff = Column(Float, nullable=True, comment="왼쪽 어깨 높이 차이 (mm)")
    
    # 10. 왼쪽 견갑골 날개 (Left Scapular Winging)
    left_scapular_winging = Column(Float, nullable=True, comment="왼쪽 견갑골 날개 (도)")
    
    # 11. 오른쪽 견갑골 날개 (Right Scapular Winging)
    right_scapular_winging = Column(Float, nullable=True, comment="오른쪽 견갑골 날개 (도)")
    
    # 12. 어깨 전방 이동 (Shoulder Forward Movement)
    shoulder_forward_movement = Column(Float, nullable=True, comment="어깨 전방 이동 (도)")
    
    # 13. 머리 회전 (Head Rotation)
    head_rotation = Column(Float, nullable=True, comment="머리 회전 (도)")
    
    # ==================== 추가 정보 ====================
    # 세션 정보
    session_id = Column(BigInteger, nullable=True, comment="세션 ID")
    device_info = Column(String(200), nullable=True, comment="기기 정보")
    
    # 문제점 정보
    issues = Column(Text, nullable=True, comment="발견된 문제점들 (JSON)")
    
    # 정상 여부 판단
    is_neck_angle_normal = Column(Boolean, nullable=True, comment="목 각도 정상 여부")
    is_forward_head_normal = Column(Boolean, nullable=True, comment="전방 머리 정상 여부")
    is_head_tilt_normal = Column(Boolean, nullable=True, comment="머리 기울기 정상 여부")
    
    # 시간 정보
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="생성 시간")
    
    # 관계 설정
    user = relationship("User", back_populates="posture_records")
    
    def __repr__(self):
        return f"<PostureRecord(id={self.id}, user_id={self.user_id}, score={self.score})>"

class PostureAnalysis(Base):
    """
    자세 분석 결과 모델
    
    자세 측정 기록에 대한 분석 결과와 통계를 저장
    """
    __tablename__ = "posture_analyses"
    
    id = Column(Integer, primary_key=True, index=True, comment="분석 고유 ID")
    record_id = Column(Integer, ForeignKey("posture_records.id"), nullable=False, comment="기록 ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="사용자 ID")
    
    # ==================== 종합 평가 ====================
    overall_score = Column(Float, nullable=True, comment="종합 자세 점수 (0-100)")
    overall_grade = Column(String(10), nullable=True, comment="종합 등급 (A, B, C, D, F)")
    risk_level = Column(String(20), nullable=True, comment="위험도 (Low, Medium, High)")
    
    # ==================== 개별 지표 평가 ====================
    neck_score = Column(Float, nullable=True, comment="목 각도 점수")
    shoulder_score = Column(Float, nullable=True, comment="어깨 각도 점수")
    back_score = Column(Float, nullable=True, comment="등 각도 점수")
    hip_score = Column(Float, nullable=True, comment="엉덩이 각도 점수")
    knee_score = Column(Float, nullable=True, comment="무릎 각도 점수")
    ankle_score = Column(Float, nullable=True, comment="발목 각도 점수")
    
    # ==================== 문제점 분석 ====================
    issues = Column(JSON, nullable=True, comment="발견된 문제점 목록")
    recommendations = Column(JSON, nullable=True, comment="개선 권장사항")
    
    # ==================== 분석 메타데이터 ====================
    analysis_time = Column(DateTime(timezone=True), server_default=func.now(), comment="분석 시간")
    analysis_version = Column(String(20), nullable=True, comment="분석 알고리즘 버전")
    
    # 관계 설정
    user = relationship("User", back_populates="posture_analyses")
    
    def __repr__(self):
        return f"<PostureAnalysis(id={self.id}, record_id={self.record_id}, score={self.overall_score})>" 