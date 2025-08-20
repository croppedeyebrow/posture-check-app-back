#!/usr/bin/env python3
"""
데이터베이스 마이그레이션 스크립트
기존 테이블에 새로운 컬럼들을 안전하게 추가합니다.
"""

import os
import sys
from sqlalchemy import text, inspect
from app.db.session import engine
from app.db.base import Base

def check_column_exists(table_name, column_name):
    """컬럼이 존재하는지 확인"""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def migrate_posture_records():
    """posture_records 테이블 마이그레이션"""
    print("posture_records 테이블 마이그레이션 시작...")
    
    # 추가할 컬럼들
    new_columns = [
        ('score', 'FLOAT'),  # 점수 컬럼 추가
        ('shoulder_slope', 'FLOAT'),
        ('head_forward', 'FLOAT'),
        ('cervical_lordosis', 'FLOAT'),
        ('forward_head_distance', 'FLOAT'),
        ('head_tilt', 'FLOAT'),
        ('left_shoulder_height_diff', 'FLOAT'),
        ('left_scapular_winging', 'FLOAT'),
        ('right_scapular_winging', 'FLOAT'),
        ('shoulder_forward_movement', 'FLOAT'),
        ('head_rotation', 'FLOAT'),
        ('session_id', 'VARCHAR(100)'),
        ('device_info', 'VARCHAR(200)'),
        ('issues', 'TEXT'),
        ('is_neck_angle_normal', 'BOOLEAN'),
        ('is_forward_head_normal', 'BOOLEAN'),
        ('is_head_tilt_normal', 'BOOLEAN')
    ]
    
    with engine.connect() as conn:
        for column_name, column_type in new_columns:
            if not check_column_exists('posture_records', column_name):
                print(f"컬럼 추가: {column_name}")
                sql = f"ALTER TABLE posture_records ADD COLUMN {column_name} {column_type}"
                conn.execute(text(sql))
                conn.commit()
            else:
                print(f"컬럼 이미 존재: {column_name}")
    
    print("posture_records 테이블 마이그레이션 완료!")

def main():
    """메인 함수"""
    try:
        print("데이터베이스 마이그레이션 시작...")
        
        # 테이블이 없으면 생성
        Base.metadata.create_all(bind=engine)
        print("기본 테이블 생성 완료")
        
        # posture_records 테이블 마이그레이션
        migrate_posture_records()
        
        print("모든 마이그레이션 완료!")
        
    except Exception as e:
        print(f"마이그레이션 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
