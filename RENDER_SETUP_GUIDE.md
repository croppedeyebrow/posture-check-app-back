# 🎯 Render 환경 변수 설정 가이드

## 📋 Railway에서 Render로 환경 변수 설정하기

### 1단계: Railway 환경 변수 복사

Railway 대시보드에서 `MYSQL_PUBLIC_URL` 값을 복사하세요:

```
MYSQL_PUBLIC_URL=mysql://root:UjAzdcBnlPboaTcSxGraxSklwAUFFLMC@switchyard.proxy.rlwy.net:44749/railway
```

### 2단계: Render 환경 변수 설정

1. **Render 대시보드 접속**

   - [Render Dashboard](https://dashboard.render.com)에서 프로젝트 선택

2. **Environment 섹션으로 이동**

   - 왼쪽 메뉴에서 "Environment" 클릭

3. **환경 변수 추가**
   다음 변수들을 하나씩 추가하세요:

   | Key                           | Value                                                                                   |
   | ----------------------------- | --------------------------------------------------------------------------------------- |
   | `DATABASE_URL`                | `mysql://root:UjAzdcBnlPboaTcSxGraxSklwAUFFLMC@switchyard.proxy.rlwy.net:44749/railway` |
   | `BACKEND_CORS_ORIGINS`        | `https://posture-check-app.vercel.app,http://localhost:3000,http://localhost:8080`      |
   | `SECRET_KEY`                  | `posture-app-secret-key-2024` (또는 자동 생성)                                          |
   | `ALGORITHM`                   | `HS256`                                                                                 |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | `30`                                                                                    |
   | `USE_LOCAL_CONFIG`            | `false`                                                                                 |

**중요**: Railway의 `MYSQL_PUBLIC_URL` 값을 Render의 `DATABASE_URL`로 설정합니다!

### 3단계: 설정 확인

1. **변수 추가 후 "Save Changes" 클릭**
2. **자동 재배포 확인**
   - Render가 자동으로 새로운 환경 변수로 재배포를 시작합니다
3. **배포 완료 대기**
   - 배포 상태가 "Live"가 될 때까지 기다립니다

### 4단계: 연결 테스트

```bash
# 헬스 체크
curl https://your-app-name.onrender.com/health

# 예상 응답:
{
  "status": "healthy",
  "database": "connected",
  "message": "애플리케이션이 정상적으로 작동 중입니다."
}
```

## 🔧 문제 해결

### 연결 오류가 발생하는 경우

1. **환경 변수 확인**

   - `DATABASE_URL`에 Railway의 `MYSQL_PUBLIC_URL` 값 사용 확인
   - 포트 번호가 `44749`인지 확인

2. **Railway 상태 확인**

   - Railway 대시보드에서 MySQL 서비스가 "Deployed" 상태인지 확인

3. **로그 확인**
   - Render 대시보드에서 "Logs" 탭 확인
   - 데이터베이스 연결 오류 메시지 확인

### 일반적인 오류들

| 오류 메시지          | 해결 방법                       |
| -------------------- | ------------------------------- |
| `Connection refused` | Railway MySQL 서비스 상태 확인  |
| `Access denied`      | 비밀번호 확인                   |
| `Unknown database`   | 데이터베이스 이름 확인          |
| `Connection timeout` | DATABASE_URL의 호스트/포트 확인 |

## ✅ 성공 확인 방법

1. **헬스 체크 성공**

   ```bash
   curl https://your-app-name.onrender.com/health
   ```

2. **API 문서 접속**

   ```
   https://your-app-name.onrender.com/docs
   ```

3. **데이터베이스 테이블 생성 확인**

   - Railway 대시보드에서 MySQL 서비스의 "Connect" 탭
   - "Open Adminer" 클릭하여 테이블 확인

4. **CORS 연결 확인**
   - [Vercel 프론트엔드](https://posture-check-app.vercel.app/)에서 API 호출 테스트

## 🎉 완료!

모든 환경 변수가 올바르게 설정되면:

- ✅ FastAPI 서버가 Railway MySQL에 연결
- ✅ 데이터베이스 테이블 자동 생성
- ✅ API 엔드포인트 정상 작동
- ✅ JWT 인증 시스템 활성화
- ✅ Vercel 프론트엔드와 CORS 연결

---

**배포된 API 엔드포인트:**

- **Production URL**: `https://your-app-name.onrender.com`
- **API Docs**: `https://your-app-name.onrender.com/docs`
- **Health Check**: `https://your-app-name.onrender.com/health`
- **Frontend**: [https://posture-check-app.vercel.app/](https://posture-check-app.vercel.app/)
