# ⚡ 빠른 배포 가이드 (Render + Railway)

## 🎯 5분 만에 배포하기

### 1단계: Railway MySQL 설정 (2분)

1. [Railway](https://railway.app) 가입/로그인
2. "New Project" → "Deploy from GitHub repo"
3. "Add Service" → "Database" → "MySQL"
4. 연결 정보 복사 (Connect 탭에서)

### 2단계: Render 배포 (3분)

1. [Render](https://render.com) 가입/로그인
2. "New" → "Web Service"
3. GitHub 저장소 연결
4. 설정:

   - **Name**: `posture-app-backend`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

5. 환경 변수 설정 (Railway에서 복사한 값들):

   ```
   # Railway MySQL 연결 정보
   MYSQL_URL=mysql://root:UjAzdcBnlPboaTcSxGraxSk1wAUFFLMC@mysql.railway.internal:3306/railway
   MYSQLDATABASE=railway
   MYSQLHOST=mysql.railway.internal
   MYSQLPASSWORD=UjAzdcBnlPboaTcSxGraxSk1wAUFFLMC
   MYSQLPORT=3306
   MYSQLUSER=root

   # 보안 설정
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   USE_LOCAL_CONFIG=false
   ```

6. "Create Web Service" 클릭

### 3단계: 확인 (30초)

```bash
# 헬스 체크
curl https://your-app.onrender.com/health

# API 문서
open https://your-app.onrender.com/docs
```

## 💰 비용

- **Railway**: 월 $5 크레딧 (무료)
- **Render**: 월 750시간 (무료)
- **총 비용**: $0 (무료)

## 🔧 문제 해결

### 연결 오류

- Railway MYSQL_URL 확인
- 환경 변수 재설정

### 빌드 실패

- requirements.txt 확인
- Python 버전 확인 (3.11.0)

### 런타임 오류

- 로그 확인
- 포트 설정 확인

## 📞 지원

- **Railway**: [Discord](https://discord.gg/railway)
- **Render**: [Documentation](https://render.com/docs)
- **프로젝트**: [GitHub Issues](https://github.com/your-repo/issues)

---

**배포 완료! 🎉**
