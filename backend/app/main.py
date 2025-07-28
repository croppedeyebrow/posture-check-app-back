from fastapi import FastAPI, HTTPException
import pymysql
import os
from contextlib import contextmanager

app = FastAPI()

# 데이터베이스 연결 설정
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'user'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'database': os.getenv('DB_NAME', 'testdb'),
    'charset': 'utf8mb4'
}

@contextmanager
def get_db_connection():
    """데이터베이스 연결을 관리하는 컨텍스트 매니저"""
    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        yield connection
    except Exception as e:
        print(f"데이터베이스 연결 오류: {e}")
        raise
    finally:
        if connection:
            connection.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI + MySQL Docker Compose 연결 성공!"}

@app.get("/health")
def health_check():
    """데이터베이스 연결 상태 확인"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return {
                    "status": "healthy",
                    "database": "connected",
                    "message": "서비스가 정상적으로 작동 중입니다."
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터베이스 연결 실패: {str(e)}")

@app.get("/db-test")
def test_database():
    """데이터베이스 테스트 엔드포인트"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # 테이블 생성 (없는 경우)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS test_table (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        message VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # 테스트 데이터 삽입
                cursor.execute("INSERT INTO test_table (message) VALUES (%s)", ("Docker Compose 테스트",))
                conn.commit()
                
                # 데이터 조회
                cursor.execute("SELECT * FROM test_table ORDER BY created_at DESC LIMIT 5")
                results = cursor.fetchall()
                
                return {
                    "message": "데이터베이스 테스트 성공",
                    "data": [
                        {"id": row[0], "message": row[1], "created_at": str(row[2])}
                        for row in results
                    ]
                }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터베이스 테스트 실패: {str(e)}")
