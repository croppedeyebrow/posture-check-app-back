from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from ..models.posture import PostureRecord, PostureSession, PostureAnalysis
from ..schemas.posture import PostureRecordCreate, PostureAnalysisCreate
from ..core.config import settings

class CRUDPostureRecord:
    def create(self, db: Session, user_id: int, obj_in: PostureRecordCreate) -> PostureRecord:
        """자세 기록 생성"""
        # 의학적 기준 판단
        is_neck_angle_normal = (
            settings.NECK_ANGLE_NORMAL_MIN <= obj_in.neck_angle <= settings.NECK_ANGLE_NORMAL_MAX
        )
        is_forward_head_normal = obj_in.forward_head_distance <= settings.FORWARD_HEAD_DISTANCE_MAX
        is_head_tilt_normal = (
            settings.HEAD_TILT_NORMAL_MIN <= obj_in.head_tilt <= settings.HEAD_TILT_NORMAL_MAX
        )
        
        db_obj = PostureRecord(
            user_id=user_id,
            **obj_in.dict(),
            is_neck_angle_normal=is_neck_angle_normal,
            is_forward_head_normal=is_forward_head_normal,
            is_head_tilt_normal=is_head_tilt_normal
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_user(
        self, 
        db: Session, 
        user_id: int, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[PostureRecord]:
        """사용자의 자세 기록 조회"""
        query = db.query(PostureRecord).filter(PostureRecord.user_id == user_id)
        
        if start_date:
            query = query.filter(PostureRecord.created_at >= start_date)
        if end_date:
            query = query.filter(PostureRecord.created_at <= end_date)
        
        return query.order_by(PostureRecord.created_at.desc()).limit(limit).all()
    
    def get_stats(self, db: Session, user_id: int, days: int = 30) -> Dict:
        """자세 통계 조회"""
        start_date = datetime.now() - timedelta(days=days)
        
        # 기본 통계
        total_records = db.query(PostureRecord).filter(
            and_(
                PostureRecord.user_id == user_id,
                PostureRecord.created_at >= start_date
            )
        ).count()
        
        if total_records == 0:
            return {
                "total_records": 0,
                "average_score": 0,
                "improvement_rate": 0,
                "normal_posture_rate": 0
            }
        
        # 평균 점수
        avg_score = db.query(func.avg(PostureRecord.score)).filter(
            and_(
                PostureRecord.user_id == user_id,
                PostureRecord.created_at >= start_date
            )
        ).scalar()
        
        # 정상 자세 비율
        normal_records = db.query(PostureRecord).filter(
            and_(
                PostureRecord.user_id == user_id,
                PostureRecord.created_at >= start_date,
                PostureRecord.is_neck_angle_normal == True,
                PostureRecord.is_forward_head_normal == True,
                PostureRecord.is_head_tilt_normal == True
            )
        ).count()
        
        normal_rate = (normal_records / total_records) * 100 if total_records > 0 else 0
        
        # 개선률 계산
        recent_start = datetime.now() - timedelta(days=7)
        previous_start = recent_start - timedelta(days=7)
        
        recent_avg = db.query(func.avg(PostureRecord.score)).filter(
            and_(
                PostureRecord.user_id == user_id,
                PostureRecord.created_at >= recent_start
            )
        ).scalar() or 0
        
        previous_avg = db.query(func.avg(PostureRecord.score)).filter(
            and_(
                PostureRecord.user_id == user_id,
                PostureRecord.created_at >= previous_start,
                PostureRecord.created_at < recent_start
            )
        ).scalar() or 0
        
        improvement_rate = ((recent_avg - previous_avg) / previous_avg * 100) if previous_avg > 0 else 0
        
        return {
            "total_records": total_records,
            "average_score": round(avg_score, 2) if avg_score else 0,
            "improvement_rate": round(improvement_rate, 2),
            "normal_posture_rate": round(normal_rate, 2)
        }
    
    def get_trends(self, db: Session, user_id: int, days: int = 7) -> List[Dict]:
        """자세 변화 트렌드 조회"""
        start_date = datetime.now() - timedelta(days=days)
        
        daily_stats = db.query(
            func.date(PostureRecord.created_at).label('date'),
            func.avg(PostureRecord.score).label('avg_score'),
            func.count(PostureRecord.id).label('record_count'),
            func.avg(PostureRecord.neck_angle).label('neck_angle_avg'),
            func.avg(PostureRecord.forward_head_distance).label('forward_head_avg')
        ).filter(
            and_(
                PostureRecord.user_id == user_id,
                PostureRecord.created_at >= start_date
            )
        ).group_by(func.date(PostureRecord.created_at)).all()
        
        return [
            {
                "date": str(stat.date),
                "average_score": round(stat.avg_score, 2) if stat.avg_score else 0,
                "record_count": stat.record_count,
                "neck_angle_avg": round(stat.neck_angle_avg, 2) if stat.neck_angle_avg else 0,
                "forward_head_distance_avg": round(stat.forward_head_avg, 2) if stat.forward_head_avg else 0
            }
            for stat in daily_stats
        ]

class CRUDPostureAnalysis:
    def create(self, db: Session, user_id: int, obj_in: PostureAnalysisCreate) -> PostureAnalysis:
        """자세 분석 결과 생성"""
        db_obj = PostureAnalysis(
            user_id=user_id,
            **obj_in.dict()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

# CRUD 인스턴스
posture_record = CRUDPostureRecord()
posture_analysis = CRUDPostureAnalysis() 