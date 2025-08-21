#!/usr/bin/env python3
"""
배포 환경용 데이터베이스 초기화 스크립트
Render/Railway 배포 시 사용
"""

import os
import sys

def main():
    """메인 함수"""
    print("=== 배포 환경 데이터베이스 초기화 ===")
    
    try:
        # 배포 환경 설정
        os.environ["USE_LOCAL_CONFIG"] = "false"
        
        from app.db.session import init_db, engine
        from sqlalchemy import text
        
        # 데이터베이스 연결 테스트
        print("🔗 데이터베이스 연결 테스트...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ 데이터베이스 연결 성공")
        
        # 기존 테이블 삭제 후 새로 생성 (깨끗한 상태로 시작)
        print("🔄 기존 테이블 삭제 중...")
        with engine.connect() as conn:
            try:
                conn.execute(text("DROP TABLE IF EXISTS posture_records"))
                conn.execute(text("DROP TABLE IF EXISTS posture_sessions"))
                conn.execute(text("DROP TABLE IF EXISTS posture_analyses"))
                conn.commit()
                print("✅ 기존 테이블 삭제 완료")
            except Exception as e:
                print(f"ℹ️ 테이블 삭제 중 오류 (무시): {e}")
        
        # 테이블 새로 생성 (직접 SQL로 생성하여 최신 스키마 적용)
        print("🔄 테이블 새로 생성 중...")
        with engine.connect() as conn:
            # posture_records 테이블 생성 (session_id를 VARCHAR(50)으로)
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS posture_records (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    neck_angle FLOAT,
                    shoulder_slope FLOAT,
                    head_forward FLOAT,
                    shoulder_height_diff FLOAT,
                    score FLOAT,
                    cervical_lordosis FLOAT,
                    forward_head_distance FLOAT,
                    head_tilt FLOAT,
                    left_shoulder_height_diff FLOAT,
                    left_scapular_winging FLOAT,
                    right_scapular_winging FLOAT,
                    shoulder_forward_movement FLOAT,
                    head_rotation FLOAT,
                    session_id VARCHAR(50),
                    device_info VARCHAR(200),
                    issues TEXT,
                    is_neck_angle_normal BOOLEAN,
                    is_forward_head_normal BOOLEAN,
                    is_head_tilt_normal BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """))
            conn.commit()
        print("✅ 테이블 새로 생성 완료")
        
        # 새로 생성된 테이블 구조 확인
        print("🔧 새로 생성된 테이블 구조 확인 중...")
        with engine.connect() as conn:
            result = conn.execute(text("DESCRIBE posture_records"))
            columns = result.fetchall()
            print("posture_records 테이블 컬럼:")
            for col in columns:
                print(f"  - {col[0]}: {col[1]}")
        
        # 생성된 테이블 확인
        print("\n📋 생성된 테이블 목록:")
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            for table in tables:
                print(f"  - {table[0]}")
        
        print("\n🎉 배포 환경 데이터베이스 초기화 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
