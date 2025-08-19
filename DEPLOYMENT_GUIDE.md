# 🚀 배포 가이드 (Render + Railway)

이 가이드는 Posture Check App Backend를 Render와 Railway를 사용하여 배포하는 방법을 설명합니다.

## 📋 배포 구성

- **Backend API**: Render (FastAPI)
- **Database**: Railway (MySQL)

## 🔧 사전 준비

### 1. Railway 데이터베이스 설정

1. [Railway](https://railway.app)에 가입
2. 새 프로젝트 생성
3. MySQL 데이터베이스 추가:
   - "Add Service" → "Database" → "MySQL"
   - 데이터베이스 이름 설정
   - 연결 정보 확인

### 2. Render 계정 설정

1. [Render](https://render.com)에 가입
2. GitHub 저장소 연결

## 🚀 배포 단계

### 1. Railway MySQL 데이터베이스 설정

1. **Railway 프로젝트 생성**

   - [Railway Dashboard](https://railway.app/dashboard)에서 새 프로젝트 생성
   - "Add Service" → "Database" → "MySQL" 선택

2. **데이터베이스 설정**

   - 데이터베이스 이름: `posture_app_db`
   - 지역 선택 (가까운 지역 권장)
   - "Deploy" 클릭

3. **연결 정보 확인**
   - 데이터베이스 서비스에서 "Connect" 탭 확인
   - 다음 환경 변수들을 복사:
     - `MYSQL_URL`
     - `MYSQLDATABASE`
     - `MYSQLHOST`
     - `MYSQLPASSWORD`
     - `MYSQLPORT`
     - `MYSQLUSER`

### 2. Render 배포

1. **새 Web Service 생성**

   - GitHub 저장소 연결
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **환경 변수 설정**

   ```
   # Railway MySQL 연결 정보
   MYSQL_URL=mysql://root:password@mysql.railway.internal:3306/database
   MYSQLDATABASE=database
   MYSQLHOST=mysql.railway.internal
   MYSQLPASSWORD=password
   MYSQLPORT=3306
   MYSQLUSER=root

   # 보안 설정
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   USE_LOCAL_CONFIG=false
   ```

3. **고급 설정**
   - Auto-Deploy: Yes
   - Branch: main

### 3. 데이터베이스 마이그레이션

배포 후 데이터베이스 테이블이 자동으로 생성됩니다.

## 🔍 배포 확인

### 1. 헬스 체크

```bash
curl https://your-app-name.onrender.com/health
```

### 2. API 문서

```
https://your-app-name.onrender.com/docs
```

### 3. 루트 엔드포인트

```bash
curl https://your-app-name.onrender.com/
```

## 🔧 환경 변수 설명

| 변수명                        | 설명                      | 예시                               |
| ----------------------------- | ------------------------- | ---------------------------------- |
| `MYSQL_URL`                   | Railway MySQL 연결 문자열 | `mysql://root:pass@host:port/db`   |
| `MYSQLDATABASE`               | 데이터베이스 이름         | `railway`                          |
| `MYSQLHOST`                   | 데이터베이스 호스트       | `mysql.railway.internal`           |
| `MYSQLPASSWORD`               | 데이터베이스 비밀번호     | `UjAzdcBnlPboaTcSxGraxSk1wAUFFLMC` |
| `MYSQLPORT`                   | 데이터베이스 포트         | `3306`                             |
| `MYSQLUSER`                   | 데이터베이스 사용자       | `root`                             |
| `SECRET_KEY`                  | JWT 토큰 암호화 키        | 자동 생성됨                        |
| `ALGORITHM`                   | JWT 알고리즘              | `HS256`                            |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 토큰 만료 시간            | `30`                               |
| `USE_LOCAL_CONFIG`            | 로컬 설정 사용 여부       | `false`                            |

## 🛠️ 문제 해결

### 1. 데이터베이스 연결 오류

- Railway MYSQL_URL 확인
- 데이터베이스 서비스 상태 확인
- Railway 대시보드에서 연결 상태 확인

### 2. 빌드 실패

- requirements.txt 의존성 확인
- Python 버전 확인 (3.11.0)
- 로그 확인

### 3. 런타임 오류

- 환경 변수 설정 확인
- 포트 설정 확인
- 로그 확인

## 📊 모니터링

### 1. Render 대시보드

- 로그 확인
- 성능 메트릭
- 오류 알림

### 2. Railway 대시보드

- 데이터베이스 성능
- 연결 상태
- 사용량 모니터링

## 🔄 업데이트

1. GitHub에 코드 푸시
2. Render 자동 배포 확인
3. 헬스 체크로 정상 작동 확인

## 💰 비용 관리

### Railway 무료 티어

- 월 $5 크레딧 제공
- MySQL 데이터베이스: $5/월
- **결론**: 무료 티어로 충분히 사용 가능

### Render 무료 티어

- 월 750시간 무료
- 15분 비활성 후 슬립
- **결론**: 개발/테스트용으로 적합

## 📞 지원

문제가 발생하면 다음을 확인하세요:

1. Render 로그
2. Railway 연결 상태
3. 환경 변수 설정
4. API 문서 (`/docs`)

---

**배포 완료 후 API 엔드포인트:**

- Production URL: `https://your-app-name.onrender.com`
- API Docs: `https://your-app-name.onrender.com/docs`
- Health Check: `https://your-app-name.onrender.com/health`

## 🎯 Railway vs PlanetScale 비교

| 기능           | Railway      | PlanetScale |
| -------------- | ------------ | ----------- |
| 무료 티어      | $5/월 크레딧 | 제한적      |
| MySQL 지원     | ✅           | ✅          |
| 자동 백업      | ✅           | ✅          |
| SSL 연결       | ✅           | ✅          |
| 설정 난이도    | 쉬움         | 보통        |
| 한국 접속 속도 | 빠름         | 보통        |
