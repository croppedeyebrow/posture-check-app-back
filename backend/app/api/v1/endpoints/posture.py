from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json
import uuid
import time

from ....db.session import get_db
from ....schemas.posture import (
    PostureRecordCreate, PostureRecord, PostureStats, PostureTrend, MedicalStandards,
    PostureDataSave, PostureAnalysisConfig, PostureAnalysisSession
)
from ....crud.posture import posture_record
from ....core.config import settings

router = APIRouter()

# 활성 세션 저장소 (실제 프로덕션에서는 Redis나 DB 사용 권장)
active_sessions = {}

@router.post("/save", response_model=PostureRecord)
def save_posture_data(
    posture_data: PostureDataSave,
    db: Session = Depends(get_db)
):
    """웹캠을 통한 자세 측정 데이터 저장"""
    try:
        print(f"받은 데이터: {posture_data}")
        
        # issues를 JSON 문자열로 변환 (dict 리스트를 문자열 리스트로 변환)
        issues_list = []
        if posture_data.issues:
            for issue in posture_data.issues:
                if isinstance(issue, dict):
                    # dict에서 필요한 정보 추출 (예: message, type 등)
                    if 'message' in issue:
                        issues_list.append(issue['message'])
                    elif 'type' in issue:
                        issues_list.append(issue['type'])
                    else:
                        issues_list.append(str(issue))
                else:
                    issues_list.append(str(issue))
        issues_json = json.dumps(issues_list)
        
        print(f"변환된 issues: {issues_json}")
        
        # PostureRecordCreate 형태로 변환 (camelCase에서 snake_case로 변환)
        record_data = PostureRecordCreate(
            neck_angle=posture_data.neckAngle,
            shoulder_slope=posture_data.shoulderSlope,
            head_forward=posture_data.headForward,
            shoulder_height_diff=posture_data.shoulderHeightDiff,
            score=posture_data.score,
            cervical_lordosis=posture_data.cervicalLordosis,
            forward_head_distance=posture_data.forwardHeadDistance,
            head_tilt=posture_data.headTilt,
            left_shoulder_height_diff=0.0,  # 기본값 설정
            left_scapular_winging=0.0,      # 기본값 설정
            right_scapular_winging=0.0,     # 기본값 설정
            shoulder_forward_movement=posture_data.shoulderForwardMovement,
            head_rotation=posture_data.headRotation,
            issues=issues_json,
            session_id=posture_data.sessionId or str(int(time.time())),
            device_info=posture_data.deviceInfo
        )
        
        print(f"생성된 record_data: {record_data}")
        
        result = posture_record.create(db, posture_data.userId, record_data)
        
        # issues 필드를 JSON 문자열로 유지 (데이터베이스에서 가져온 그대로)
        # result.issues는 이미 JSON 문자열이므로 그대로 사용
        
        return result
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"오류 발생: {str(e)}")
        print(f"오류 상세: {error_traceback}")
        raise HTTPException(status_code=500, detail=f"자세 데이터 저장 실패: {str(e)}")

@router.post("/analysis/start", response_model=PostureAnalysisSession)
def start_posture_analysis(
    config: PostureAnalysisConfig,
    db: Session = Depends(get_db)
):
    """실시간 자세 분석 세션 시작"""
    try:
        session_id = config.session_id or str(int(time.time()))
        
        # 세션 정보 생성
        session_info = PostureAnalysisSession(
            session_id=session_id,
            user_id=config.user_id,
            start_time=datetime.now(),
            status="active",
            device_info=config.device_info
        )
        
        # 활성 세션에 저장
        active_sessions[session_id] = {
            "user_id": config.user_id,
            "start_time": session_info.start_time,
            "status": "active",
            "device_info": config.device_info,
            "analysis_interval": config.analysis_interval,
            "record_count": 0
        }
        
        return session_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"자세 분석 세션 시작 실패: {str(e)}")

@router.post("/analysis/stop")
def stop_posture_analysis(
    session_id: str,
    db: Session = Depends(get_db)
):
    """실시간 자세 분석 세션 중지"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다")
        
        # 세션 상태 업데이트
        active_sessions[session_id]["status"] = "stopped"
        active_sessions[session_id]["end_time"] = datetime.now()
        
        # 세션 통계 계산
        session_data = active_sessions[session_id]
        duration = (session_data["end_time"] - session_data["start_time"]).total_seconds()
        
        return {
            "session_id": session_id,
            "status": "stopped",
            "duration_seconds": int(duration),
            "total_records": session_data["record_count"],
            "message": "자세 분석 세션이 성공적으로 중지되었습니다"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"자세 분석 세션 중지 실패: {str(e)}")

@router.get("/analysis/sessions")
def get_active_sessions():
    """활성 분석 세션 목록 조회"""
    try:
        active_list = []
        for session_id, session_data in active_sessions.items():
            if session_data["status"] == "active":
                active_list.append({
                    "session_id": session_id,
                    "user_id": session_data["user_id"],
                    "start_time": session_data["start_time"],
                    "device_info": session_data["device_info"],
                    "record_count": session_data["record_count"]
                })
        
        return {
            "active_sessions": active_list,
            "total_active": len(active_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"활성 세션 조회 실패: {str(e)}")

@router.post("/record", response_model=PostureRecord)
def create_posture_record(
    record: PostureRecordCreate,
    user_id: int = Query(..., description="사용자 ID"),
    db: Session = Depends(get_db)
):
    """자세 기록 생성"""
    try:
        result = posture_record.create(db, user_id, record)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"자세 기록 생성 실패: {str(e)}")

@router.get("/records", response_model=List[PostureRecord])
def get_posture_records(
    user_id: int = Query(..., description="사용자 ID"),
    start_date: Optional[str] = Query(None, description="시작 날짜 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="종료 날짜 (YYYY-MM-DD)"),
    limit: int = Query(100, description="조회할 기록 수"),
    db: Session = Depends(get_db)
):
    """사용자의 자세 기록 조회"""
    try:
        # 날짜 파싱
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
        
        records = posture_record.get_by_user(db, user_id, start_dt, end_dt, limit)
        return records
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"날짜 형식 오류: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"자세 기록 조회 실패: {str(e)}")

@router.get("/stats", response_model=PostureStats)
def get_posture_stats(
    user_id: int = Query(..., description="사용자 ID"),
    days: int = Query(30, description="통계 기간 (일)"),
    db: Session = Depends(get_db)
):
    """자세 통계 조회"""
    try:
        stats = posture_record.get_stats(db, user_id, days)
        return PostureStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"자세 통계 조회 실패: {str(e)}")

@router.get("/trends", response_model=List[PostureTrend])
def get_posture_trends(
    user_id: int = Query(..., description="사용자 ID"),
    days: int = Query(7, description="트렌드 기간 (일)"),
    db: Session = Depends(get_db)
):
    """자세 변화 트렌드 조회"""
    try:
        trends = posture_record.get_trends(db, user_id, days)
        return [PostureTrend(**trend) for trend in trends]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"자세 트렌드 조회 실패: {str(e)}")

@router.post("/analyze")
def analyze_posture(
    record: PostureRecordCreate
):
    """자세 분석 (실시간)"""
    try:
        # 의학적 기준 판단
        is_neck_angle_normal = (
            settings.NECK_ANGLE_NORMAL_MIN <= record.neck_angle <= settings.NECK_ANGLE_NORMAL_MAX
        )
        is_forward_head_normal = record.forward_head_distance <= settings.FORWARD_HEAD_DISTANCE_MAX
        is_head_tilt_normal = (
            settings.HEAD_TILT_NORMAL_MIN <= record.head_tilt <= settings.HEAD_TILT_NORMAL_MAX
        )
        
        # 문제점 분석
        problems = []
        suggestions = []
        
        if not is_neck_angle_normal:
            problems.append("목 각도가 정상 범위를 벗어났습니다")
            suggestions.append("목을 중앙으로 돌려주세요")
        
        if not is_forward_head_normal:
            problems.append("머리가 너무 앞으로 나와있습니다")
            suggestions.append("턱을 뒤로 당겨주세요")
        
        if not is_head_tilt_normal:
            problems.append("머리가 측면으로 기울어져 있습니다")
            suggestions.append("머리를 중앙으로 정렬해주세요")
        
        # 심각도 판단
        problem_count = len(problems)
        if problem_count >= 2:
            severity_level = "high"
        elif problem_count == 1:
            severity_level = "medium"
        else:
            severity_level = "low"
        
        # 편차 계산
        neck_angle_deviation = abs(record.neck_angle - (settings.NECK_ANGLE_NORMAL_MIN + settings.NECK_ANGLE_NORMAL_MAX) / 2)
        forward_head_deviation = max(0, record.forward_head_distance - settings.FORWARD_HEAD_DISTANCE_MAX)
        head_tilt_deviation = abs(record.head_tilt - (settings.HEAD_TILT_NORMAL_MIN + settings.HEAD_TILT_NORMAL_MAX) / 2)
        
        return {
            "analysis": {
                "is_neck_angle_normal": is_neck_angle_normal,
                "is_forward_head_normal": is_forward_head_normal,
                "is_head_tilt_normal": is_head_tilt_normal,
                "problems": problems,
                "suggestions": suggestions,
                "severity_level": severity_level
            },
            "deviations": {
                "neck_angle_deviation": neck_angle_deviation,
                "forward_head_deviation": forward_head_deviation,
                "head_tilt_deviation": head_tilt_deviation
            },
            "medical_standards": {
                "neck_angle_range": (settings.NECK_ANGLE_NORMAL_MIN, settings.NECK_ANGLE_NORMAL_MAX),
                "forward_head_max": settings.FORWARD_HEAD_DISTANCE_MAX,
                "head_tilt_range": (settings.HEAD_TILT_NORMAL_MIN, settings.HEAD_TILT_NORMAL_MAX)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"자세 분석 실패: {str(e)}")

@router.get("/medical-standards")
def get_medical_standards():
    """의학적 기준 조회"""
    standards = MedicalStandards()
    return {
        "neck_angle_normal_range": standards.neck_angle_normal_range,
        "forward_head_normal_max": standards.forward_head_normal_max,
        "head_tilt_normal_range": standards.head_tilt_normal_range,
        "description": {
            "neck_angle": "목 각도 정상 범위 (도)",
            "forward_head_distance": "전방 머리 거리 최대 정상값 (mm)",
            "head_tilt": "머리 기울기 정상 범위 (도)"
        }
    } 