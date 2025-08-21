#!/usr/bin/env python3
"""
데이터베이스 초기화 스크립트
기존 init_db 함수 사용 - 모든 환경에서 동일
"""

import os
import sys

def main():
    """메인 함수"""
    print("=== 데이터베이스 초기화 ===")
    
    try:
        from app.db.session import init_db, engine
        
        # 데이터베이스 연결 테스트
        print("🔗 데이터베이스 연결 테스트...")
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("✅ 데이터베이스 연결 성공")
        
        # 테이블 생성 (기존 init_db 함수 사용)
        print("🔄 테이블 생성 중...")
        init_db()
        print("✅ 테이블 생성 완료")
        
        # 생성된 테이블 확인
        print("\n📋 생성된 테이블 목록:")
        with engine.connect() as conn:
            result = conn.execute("SHOW TABLES")
            tables = result.fetchall()
            for table in tables:
                print(f"  - {table[0]}")
        
        print("\n🎉 데이터베이스 초기화 완료!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
