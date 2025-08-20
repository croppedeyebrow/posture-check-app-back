# API 연결 가이드

## 백엔드 서버 정보

### 프로덕션 서버
- **URL**: `https://posture-check-app-back.onrender.com`
- **상태**: ✅ 활성화됨
- **데이터베이스**: ✅ 연결됨 (Railway MySQL)

### 테스트 엔드포인트

#### 1. 기본 연결 테스트
```bash
GET https://posture-check-app-back.onrender.com/
```

#### 2. 헬스 체크
```bash
GET https://posture-check-app-back.onrender.com/health
```

#### 3. API 연결 테스트
```bash
GET https://posture-check-app-back.onrender.com/api/test
```

#### 4. API 문서
```bash
GET https://posture-check-app-back.onrender.com/docs
```

## 주요 API 엔드포인트

### 사용자 관리
- **회원가입**: `POST /api/v1/users/register`
- **로그인**: `POST /api/v1/users/login`
- **사용자 정보**: `GET /api/v1/users/me`
- **사용자 업데이트**: `PUT /api/v1/users/me`

### 자세 관리
- **자세 기록**: `POST /api/v1/posture/`
- **자세 조회**: `GET /api/v1/posture/`
- **자세 통계**: `GET /api/v1/posture/stats`

## 프론트엔드 설정

### 환경 변수 설정
```javascript
// .env 파일
VITE_API_BASE_URL=https://posture-check-app-back.onrender.com
```

### API 클라이언트 설정
```javascript
// api.js 또는 axios 설정
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://posture-check-app-back.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

## CORS 설정

백엔드에서 다음 도메인들을 허용하도록 설정되어 있습니다:

- `http://localhost:3000` (로컬 개발)
- `http://localhost:5173` (Vite 개발)
- `https://posture-check-app.vercel.app` (Vercel 배포)
- `https://posture-check-app-git-main-croppedeyebrow.vercel.app` (Vercel 배포)
- `*` (모든 도메인 - 개발 중)

## 문제 해결

### 1. CORS 오류가 발생하는 경우
- 프론트엔드 도메인이 허용 목록에 있는지 확인
- 브라우저 개발자 도구에서 네트워크 탭 확인

### 2. API 연결 실패
- 백엔드 서버 상태 확인: `/health` 엔드포인트 호출
- 네트워크 연결 확인
- API URL이 올바른지 확인

### 3. 인증 오류
- JWT 토큰이 올바르게 전송되는지 확인
- Authorization 헤더 설정 확인

## 테스트 방법

### 1. 브라우저에서 직접 테스트
```bash
# 헬스 체크
curl https://posture-check-app-back.onrender.com/health

# API 테스트
curl https://posture-check-app-back.onrender.com/api/test
```

### 2. Postman 또는 Insomnia에서 테스트
- Collection 생성
- 환경 변수 설정
- API 엔드포인트 테스트

### 3. 프론트엔드에서 테스트
```javascript
// 간단한 연결 테스트
fetch('https://posture-check-app-back.onrender.com/api/test')
  .then(response => response.json())
  .then(data => console.log('API 연결 성공:', data))
  .catch(error => console.error('API 연결 실패:', error));
```

## 최신 상태

- ✅ 서버 배포 완료
- ✅ 데이터베이스 연결 성공
- ✅ CORS 설정 완료
- ✅ HEAD 메서드 지원 추가
- ✅ API 엔드포인트 준비 완료
