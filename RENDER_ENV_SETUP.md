# Render 환경 변수 설정 가이드

## 필수 환경 변수

Render 대시보드에서 다음 환경 변수들을 설정해야 합니다:

### 1. 데이터베이스 연결 (선택 1개)

#### 옵션 A: DATABASE_URL 사용 (권장)
```
DATABASE_URL=mysql://username:password@host:port/database_name
```

#### 옵션 B: MYSQL_PUBLIC_URL 사용
```
MYSQL_PUBLIC_URL=mysql://username:password@host:port/database_name
```

#### 옵션 C: 개별 설정
```
DB_HOST=your-database-host
DB_PORT=3306
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-database-name
```

### 2. 보안 설정
```
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. CORS 설정
```
BACKEND_CORS_ORIGINS=*
```

## 설정 방법

1. Render 대시보드에서 해당 서비스로 이동
2. "Environment" 탭 클릭
3. "Environment Variables" 섹션에서 위의 변수들을 추가
4. "Save Changes" 클릭
5. 서비스 재배포

## 데이터베이스 서비스 추천

### 1. Railway MySQL
- Railway에서 MySQL 서비스 생성
- `MYSQL_PUBLIC_URL` 환경 변수 사용

### 2. PlanetScale
- PlanetScale에서 데이터베이스 생성
- `DATABASE_URL` 환경 변수 사용

### 3. AWS RDS
- AWS RDS MySQL 인스턴스 생성
- 개별 설정 변수 사용

## 문제 해결

### 데이터베이스 연결 오류가 발생하는 경우:
1. 환경 변수가 올바르게 설정되었는지 확인
2. 데이터베이스 서비스가 실행 중인지 확인
3. 방화벽 설정 확인
4. 데이터베이스 사용자 권한 확인

### 헬스 체크 엔드포인트 확인:
```
GET https://your-app.onrender.com/health
```

이 엔드포인트에서 데이터베이스 연결 상태를 확인할 수 있습니다.
