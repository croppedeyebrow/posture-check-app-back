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
        
        # 테이블 생성
        print("🔄 테이블 생성 중...")
        init_db()
        print("✅ 테이블 생성 완료")
        
        # created_at 컬럼 추가 (기존 테이블에 없으면)
        print("🔧 created_at 컬럼 확인 및 추가 중...")
        with engine.connect() as conn:
            # created_at 컬럼 존재 여부 확인
            result = conn.execute(text("SHOW COLUMNS FROM posture_records LIKE 'created_at'"))
            if not result.fetchall():
                # created_at 컬럼 추가
                conn.execute(text("""
                    ALTER TABLE posture_records 
                    ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
                    COMMENT '생성 시간'
                """))
                conn.commit()
                print("✅ created_at 컬럼 추가 완료")
            else:
                print("ℹ️ created_at 컬럼이 이미 존재합니다")
        
        # session_id 컬럼 타입 확인
        print("🔧 session_id 컬럼 타입 확인 중...")
        with engine.connect() as conn:
            result = conn.execute(text("SHOW COLUMNS FROM posture_records LIKE 'session_id'"))
            session_id_info = result.fetchone()
            if session_id_info:
                column_type = session_id_info[1]
                print(f"현재 session_id 타입: {column_type}")
                print("ℹ️ session_id 컬럼이 이미 존재합니다")
            else:
                print("ℹ️ session_id 컬럼이 없습니다 (새 테이블 생성 시 INT로 생성됨)")
        
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
