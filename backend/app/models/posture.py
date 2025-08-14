"""
Posture Check App Backend - 자세 관련 데이터베이스 모델

이 모듈은 자세 교정 앱의 핵심 데이터 모델을 정의합니다.
- PostureRecord: 13개 자세 지표를 저장하는 메인 테이블
- PostureSession: 측정 세션 정보 관리
- PostureAnalysis: 자세 분석 결과 저장

프론트엔드의 13개 데이터 필드와 완전히 호환되도록 설계되었습니다.
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from ..db.base import Base

class PostureRecord(Base):
    """
    자세 기록 테이블 - 프론트엔드의 13개 데이터 필드 반영
    
    자세 측정 시마다 생성되는 개별 기록을 저장합니다.
    의학적 기준에 따른 정상/비정상 판단 결과도 함께 저장됩니다.
    """
    __tablename__ = "posture_records"
    
    # ==================== 기본 정보 ====================
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # 사용자 ID (외래키)
    
    # ==================== 기존 7개 필드 (프론트엔드 호환) ====================
    neck_angle = Column(Float, comment="목 각도 (도) - 목의 전후방 기울기")
    shoulder_slope = Column(Float, comment="어깨 기울기 (도) - 양쪽 어깨의 높이 차이")
    head_forward = Column(Float, comment="머리 전방 이동 (mm) - 머리가 앞으로 나온 거리")
    shoulder_height_diff = Column(Float, comment="어깨 높이 차이 (mm) - 좌우 어깨 높이 불균형")
    score = Column(Float, comment="종합 점수 - 전체 자세 상태를 나타내는 점수")
    
    # ==================== 신규 추가 6개 필드 (의학적 정확성 향상) ====================
    cervical_lordosis = Column(Float, comment="경추 전만각 (도) - 목의 자연스러운 곡선 각도")
    forward_head_distance = Column(Float, comment="전방 머리 거리 (mm) - 머리가 몸통보다 앞으로 나온 거리")
    head_tilt = Column(Float, comment="머리 측면 기울기 (도) - 머리가 좌우로 기울어진 각도")
    left_shoulder_height_diff = Column(Float, comment="왼쪽 어깨 높이 차이 (mm) - 기준점 대비 왼쪽 어깨 높이")
    left_scapular_winging = Column(Float, comment="왼쪽 견갑골 날개 (mm) - 왼쪽 어깨뼈가 튀어나온 정도")
    right_scapular_winging = Column(Float, comment="오른쪽 견갑골 날개 (mm) - 오른쪽 어깨뼈가 튀어나온 정도")
    shoulder_forward_movement = Column(Float, comment="어깨 전방 이동 (mm) - 어깨가 앞으로 나온 거리")
    
    # ==================== 프론트엔드 추가 필드 ====================
    head_rotation = Column(Float, comment="머리 회전 (도) - 머리가 좌우로 회전한 각도")
    issues = Column(Text, comment="발견된 문제점들 (JSON 형태로 저장)")
    
    # ==================== 메타데이터 ====================
    session_id = Column(String(100), comment="세션 ID - 측정 세션을 구분하는 고유 식별자")
    device_info = Column(String(200), comment="기기 정보 - 측정에 사용된 기기 및 브라우저 정보")
    created_at = Column(DateTime, default=func.now())  # 기록 생성 시간
    
    # ==================== 의학적 기준 판단 결과 ====================
    # 실제 의료 기준에 따른 정상/비정상 판단 결과
    is_neck_angle_normal = Column(Boolean, comment="목 각도 정상 여부 (-30° ~ 30° 범위)")
    is_forward_head_normal = Column(Boolean, comment="전방 머리 거리 정상 여부 (≤ 100mm)")
    is_head_tilt_normal = Column(Boolean, comment="머리 기울기 정상 여부 (-15° ~ 15° 범위)")

class PostureSession(Base):
    """
    자세 측정 세션 테이블
    
    연속적인 자세 측정을 하나의 세션으로 관리합니다.
    세션별 통계 정보와 측정 지속 시간을 추적합니다.
    """
    __tablename__ = "posture_sessions"
    
    # ==================== 기본 정보 ====================
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # 사용자 ID
    session_id = Column(String(100), unique=True, index=True, nullable=False)  # 고유 세션 ID
    
    # ==================== 세션 시간 정보 ====================
    start_time = Column(DateTime, default=func.now())  # 세션 시작 시간
    end_time = Column(DateTime)  # 세션 종료 시간 (NULL: 진행 중)
    duration_seconds = Column(Integer, comment="세션 지속 시간(초) - 측정 총 시간")
    
    # ==================== 세션 통계 정보 ====================
    total_records = Column(Integer, default=0, comment="총 기록 수 - 이 세션에서 생성된 자세 기록 수")
    average_score = Column(Float, comment="평균 점수 - 세션 전체의 평균 자세 점수")
    
    # ==================== 메타데이터 ====================
    device_info = Column(String(200), comment="기기 정보 - 세션 측정에 사용된 기기 정보")
    created_at = Column(DateTime, default=func.now())  # 세션 생성 시간

class PostureAnalysis(Base):
    """
    자세 분석 결과 테이블
    
    자세 측정 결과에 대한 전문적인 분석 정보를 저장합니다.
    문제점 진단, 개선 제안, 심각도 평가를 포함합니다.
    """
    __tablename__ = "posture_analyses"
    
    # ==================== 기본 정보 ====================
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # 사용자 ID
    session_id = Column(String(100), nullable=False)  # 분석 대상 세션 ID
    
    # ==================== 분석 결과 ====================
    problem_description = Column(Text, comment="문제점 설명 - 발견된 자세 문제점들의 상세 설명")
    solution_suggestion = Column(Text, comment="해결책 제안 - 자세 개선을 위한 구체적인 방법 제안")
    severity_level = Column(String(20), comment="심각도 레벨 (low/medium/high) - 문제의 심각도 평가")
    
    # ==================== 의학적 기준 비교 결과 ====================
    # 실제 의료 기준 대비 편차 수치
    neck_angle_deviation = Column(Float, comment="목 각도 편차 (도) - 정상 범위 대비 편차")
    forward_head_deviation = Column(Float, comment="전방 머리 거리 편차 (mm) - 정상 범위 대비 편차")
    head_tilt_deviation = Column(Float, comment="머리 기울기 편차 (도) - 정상 범위 대비 편차")
    
    # ==================== 메타데이터 ====================
    created_at = Column(DateTime, default=func.now())  # 분석 결과 생성 시간 