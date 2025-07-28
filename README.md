# Posture Check App Backend

자세 교정 앱을 위한 FastAPI 기반 백엔드 API 서버

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 및 실행](#-설치-및-실행)
- [API 문서](#-api-문서)
- [데이터베이스 스키마](#-데이터베이스-스키마)
- [개발 가이드](#-개발-가이드)
- [프론트엔드 연동](#-프론트엔드-연동)

## 🎯 프로젝트 개요

이 프로젝트는 [posture-check-app](https://github.com/croppedeyebrow/posture-check-app) 프론트엔드와 연동되는 자세 교정 앱의 백엔드 API 서버입니다.

### 핵심 특징

- **의학적 정확성**: 실제 의료 기준을 반영한 자세 분석
- **13개 자세 지표**: 포괄적인 자세 측정 및 분석
- **실시간 처리**: 실시간 자세 감지 및 피드백
- **데이터 분석**: 통계 및 트렌드 분석 기능
- **확장 가능한 구조**: 모듈화된 아키텍처

## 🚀 주요 기능

### 1. 자세 기록 관리

- **13개 자세 지표** 저장 및 조회
- **세션 기반** 데이터 관리
- **날짜별 필터링** 및 검색 기능

### 2. 실시간 자세 분석

- **의학적 기준 기반** 자세 판단
- **정상/비정상** 자동 분류
- **개선 제안** 및 피드백 제공

### 3. 통계 및 트렌드 분석

- **개선률 계산**: 기간별 자세 개선 추이
- **정상 자세 비율**: 전체 측정 대비 정상 자세 비율
- **일별 트렌드**: 시간에 따른 자세 변화 패턴

### 4. 의학적 정확성

- **목 각도**: -30° ~ 30° (정상 범위)
- **전방 머리 거리**: ≤ 100mm (최대 정상값)
- **머리 기울기**: -15° ~ 15° (정상 범위)

## 📊 지원하는 자세 지표 (13개)

### 기존 7개 필드

| 지표명                 | 설명           | 단위  |
| ---------------------- | -------------- | ----- |
| `neck_angle`           | 목 각도        | 도(°) |
| `shoulder_slope`       | 어깨 기울기    | 도(°) |
| `head_forward`         | 머리 전방 이동 | mm    |
| `shoulder_height_diff` | 어깨 높이 차이 | mm    |
| `score`                | 종합 점수      | 점수  |

### 신규 추가 6개 필드 (의학적 정확성 향상)

| 지표명                      | 설명                | 단위  |
| --------------------------- | ------------------- | ----- |
| `cervical_lordosis`         | 경추 전만각         | 도(°) |
| `forward_head_distance`     | 전방 머리 거리      | mm    |
| `head_tilt`                 | 머리 측면 기울기    | 도(°) |
| `left_shoulder_height_diff` | 왼쪽 어깨 높이 차이 | mm    |
| `left_scapular_winging`     | 왼쪽 견갑골 날개    | mm    |
| `right_scapular_winging`    | 오른쪽 견갑골 날개  | mm    |
| `shoulder_forward_movement` | 어깨 전방 이동      | mm    |

## 🛠 기술 스택

### Backend Framework

- **FastAPI**: 고성능 Python 웹 프레임워크
- **SQLAlchemy**: Python ORM
- **Pydantic**: 데이터 검증 및 직렬화

### Database

- **MySQL 8.0**: 관계형 데이터베이스
- **Alembic**: 데이터베이스 마이그레이션

### Infrastructure

- **Docker**: 컨테이너화
- **Docker Compose**: 멀티 컨테이너 오케스트레이션

### Development Tools

- **Python 3.11**: 프로그래밍 언어
- **Uvicorn**: ASGI 서버
- **PyMySQL**: MySQL Python 드라이버

## 📁 프로젝트 구조

```
posture_app_back/
├── backend/                          # 백엔드 애플리케이션
│   ├── app/                         # 메인 애플리케이션 패키지
│   │   ├── __init__.py
│   │   ├── main.py                  # 🚀 FastAPI 애플리케이션 진입점
│   │   │
│   │   ├── core/                    # ⚙️ 설정 및 핵심 기능
│   │   │   ├── __init__.py
│   │   │   ├── config.py            # 환경 변수 및 설정 관리
│   │   │   └── security.py          # 인증, JWT, 보안 기능
│   │   │
│   │   ├── db/                      # 🗄️ 데이터베이스 관리
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # SQLAlchemy Base 클래스
│   │   │   └── session.py           # DB 연결 및 세션 관리
│   │   │
│   │   ├── models/                  # 📊 데이터베이스 모델
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # 사용자 모델
│   │   │   └── posture.py           # 자세 관련 모델 (13개 지표)
│   │   │
│   │   ├── schemas/                 # 📋 Pydantic 스키마
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # 사용자 스키마
│   │   │   └── posture.py           # 자세 관련 스키마
│   │   │
│   │   ├── crud/                    # 🔄 데이터베이스 CRUD 작업
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # 사용자 CRUD
│   │   │   └── posture.py           # 자세 관련 CRUD
│   │   │
│   │   ├── api/                     # 🌐 API 엔드포인트
│   │   │   ├── __init__.py
│   │   │   └── v1/                  # API 버전 1
│   │   │       ├── __init__.py
│   │   │       ├── routers.py       # v1 라우터 통합
│   │   │       └── endpoints/       # 실제 API 엔드포인트
│   │   │           ├── __init__.py
│   │   │           └── posture.py   # 자세 관련 API
│   │   │
│   │   └── tests/                   # 🧪 테스트 코드
│   │       └── __init__.py
│   │
│   ├── Dockerfile                   # 🐳 Docker 이미지 설정
│   ├── requirements.txt             # 📦 Python 의존성
│   └── README.md                    # 백엔드 문서
├── docker-compose.yml               # Docker Compose 설정
└── README.md                        # 프로젝트 전체 문서
```

### 핵심 파일 설명

#### 🚀 **`backend/app/main.py`**

- FastAPI 애플리케이션 설정 및 초기화
- CORS 미들웨어 구성 (프론트엔드 연동)
- API 라우터 등록 (`/api/v1` 경로)
- 헬스 체크 및 시스템 엔드포인트
- 애플리케이션 시작 시 데이터베이스 테이블 자동 생성

#### ⚙️ **`backend/app/core/config.py`**

- 환경 변수 로드 및 검증 (Pydantic BaseSettings)
- 데이터베이스 연결 설정
- 보안 설정 (JWT, 시크릿 키)
- CORS 설정
- **의학적 기준 설정** (목 각도, 전방 머리 거리, 머리 기울기)

#### 🗄️ **`backend/app/db/session.py`**

- SQLAlchemy 엔진 생성 및 설정
- 데이터베이스 세션 팩토리
- 의존성 주입을 위한 세션 제공 함수
- 데이터베이스 초기화 함수

#### 📊 **`backend/app/models/posture.py`**

- **PostureRecord**: 13개 자세 지표 저장 (프론트엔드 완전 호환)
- **PostureSession**: 측정 세션 관리
- **PostureAnalysis**: 자세 분석 결과 저장
- 의학적 기준 판단 필드 (정상/비정상 자동 분류)

#### 📋 **`backend/app/schemas/posture.py`**

- Pydantic 스키마 정의 (데이터 검증)
- API 요청/응답 형식 정의
- 13개 자세 지표 스키마
- 통계 및 트렌드 응답 스키마

#### 🔄 **`backend/app/crud/posture.py`**

- 자세 기록 CRUD 작업
- 통계 계산 서비스 (개선률, 정상 자세 비율)
- 트렌드 분석 서비스
- 의학적 기준 검증 로직

#### 🌐 **`backend/app/api/v1/endpoints/posture.py`**

- 자세 관련 API 엔드포인트 구현
- 실시간 자세 분석
- 데이터 검증 및 에러 처리
- 의학적 기준 조회 API

## 🚀 설치 및 실행

### 1. 사전 요구사항

- Docker & Docker Compose
- Git

### 2. 프로젝트 클론

```bash
git clone <repository-url>
cd posture_app_back
```

### 3. Docker Compose로 실행 (권장)

```bash
# 전체 서비스 실행
docker-compose up --build

# 백그라운드 실행
docker-compose up -d --build
```

### 4. 서비스 확인

```bash
# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f backend
```

### 5. 로컬 개발 환경 (선택사항)

```bash
# 백엔드 디렉토리로 이동
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API 문서

### 자동 생성 문서

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 API 엔드포인트

#### 자세 기록 관리

| Method | Endpoint                  | 설명             |
| ------ | ------------------------- | ---------------- |
| `POST` | `/api/v1/posture/record`  | 자세 기록 생성   |
| `GET`  | `/api/v1/posture/records` | 자세 기록 조회   |
| `GET`  | `/api/v1/posture/stats`   | 자세 통계 조회   |
| `GET`  | `/api/v1/posture/trends`  | 자세 트렌드 조회 |

#### 자세 분석

| Method | Endpoint                            | 설명             |
| ------ | ----------------------------------- | ---------------- |
| `POST` | `/api/v1/posture/analyze`           | 실시간 자세 분석 |
| `GET`  | `/api/v1/posture/medical-standards` | 의학적 기준 조회 |

#### 시스템

| Method | Endpoint    | 설명                |
| ------ | ----------- | ------------------- |
| `GET`  | `/health`   | 헬스 체크           |
| `GET`  | `/api-info` | API 정보            |
| `GET`  | `/db-test`  | 데이터베이스 테스트 |

### API 사용 예시

#### 자세 기록 생성

```bash
curl -X POST "http://localhost:8000/api/v1/posture/record?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "neck_angle": 15.5,
    "shoulder_slope": 2.3,
    "head_forward": 45.2,
    "shoulder_height_diff": 5.1,
    "score": 85.0,
    "cervical_lordosis": 12.3,
    "forward_head_distance": 85.0,
    "head_tilt": 3.2,
    "left_shoulder_height_diff": 4.8,
    "left_scapular_winging": 2.1,
    "right_scapular_winging": 1.9,
    "shoulder_forward_movement": 15.3,
    "session_id": "session_123",
    "device_info": "Chrome/Windows"
  }'
```

#### 자세 통계 조회

```bash
curl "http://localhost:8000/api/v1/posture/stats?user_id=1&days=30"
```

## 📈 데이터베이스 스키마

### 주요 테이블

#### `users` - 사용자 정보

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### `posture_records` - 자세 기록 (13개 지표)

```sql
CREATE TABLE posture_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,

    -- 기존 7개 필드
    neck_angle FLOAT COMMENT '목 각도',
    shoulder_slope FLOAT COMMENT '어깨 기울기',
    head_forward FLOAT COMMENT '머리 전방 이동',
    shoulder_height_diff FLOAT COMMENT '어깨 높이 차이',
    score FLOAT COMMENT '종합 점수',

    -- 신규 6개 필드
    cervical_lordosis FLOAT COMMENT '경추 전만각',
    forward_head_distance FLOAT COMMENT '전방 머리 거리 (mm)',
    head_tilt FLOAT COMMENT '머리 측면 기울기',
    left_shoulder_height_diff FLOAT COMMENT '왼쪽 어깨 높이 차이',
    left_scapular_winging FLOAT COMMENT '왼쪽 견갑골 날개',
    right_scapular_winging FLOAT COMMENT '오른쪽 견갑골 날개',
    shoulder_forward_movement FLOAT COMMENT '어깨 전방 이동',

    -- 메타데이터
    session_id VARCHAR(100) COMMENT '세션 ID',
    device_info VARCHAR(200) COMMENT '기기 정보',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- 의학적 기준 판단
    is_neck_angle_normal BOOLEAN COMMENT '목 각도 정상 여부',
    is_forward_head_normal BOOLEAN COMMENT '전방 머리 거리 정상 여부',
    is_head_tilt_normal BOOLEAN COMMENT '머리 기울기 정상 여부'
);
```

#### `posture_sessions` - 측정 세션

```sql
CREATE TABLE posture_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    duration_seconds INT COMMENT '세션 지속 시간(초)',
    total_records INT DEFAULT 0 COMMENT '총 기록 수',
    average_score FLOAT COMMENT '평균 점수',
    device_info VARCHAR(200) COMMENT '기기 정보',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### `posture_analyses` - 분석 결과

```sql
CREATE TABLE posture_analyses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    session_id VARCHAR(100) NOT NULL,

    -- 분석 결과
    problem_description TEXT COMMENT '문제점 설명',
    solution_suggestion TEXT COMMENT '해결책 제안',
    severity_level VARCHAR(20) COMMENT '심각도 레벨 (low/medium/high)',

    -- 의학적 기준 비교
    neck_angle_deviation FLOAT COMMENT '목 각도 편차',
    forward_head_deviation FLOAT COMMENT '전방 머리 거리 편차',
    head_tilt_deviation FLOAT COMMENT '머리 기울기 편차',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 개발 가이드

### 1. 새로운 API 추가

#### 1.1 라우터 생성

```python
# backend/app/routers/new_feature.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/new-feature", tags=["new-feature"])

@router.get("/")
def get_new_feature(db: Session = Depends(get_db)):
    return {"message": "New feature endpoint"}
```

#### 1.2 메인 앱에 등록

```python
# backend/app/main.py
from .routers import new_feature

app.include_router(new_feature.router)
```

### 2. 데이터베이스 마이그레이션

```bash
# Alembic 초기화 (최초 1회)
cd backend
alembic init alembic

# 마이그레이션 생성
alembic revision --autogenerate -m "Add new table"

# 마이그레이션 적용
alembic upgrade head
```

### 3. 환경 변수 설정

```bash
# backend/.env 파일 생성
DB_HOST=db
DB_PORT=3306
DB_USER=user
DB_PASSWORD=UserSecurePass123!
DB_NAME=testdb
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. 테스트 실행

```bash
# 테스트 실행
pytest

# 커버리지 포함 테스트
pytest --cov=app

# 특정 테스트 파일 실행
pytest tests/test_posture.py
```

## 🤝 프론트엔드 연동

### CORS 설정

현재 모든 도메인에서의 접근을 허용하도록 설정되어 있습니다:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 프론트엔드 연동 예시

#### React/Vue.js에서 API 호출

```javascript
// 자세 기록 생성
const createPostureRecord = async (recordData) => {
  const response = await fetch(
    "http://localhost:8000/api/v1/posture/record?user_id=1",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(recordData),
    }
  );
  return response.json();
};

// 자세 통계 조회
const getPostureStats = async (userId, days = 30) => {
  const response = await fetch(
    `http://localhost:8000/api/v1/posture/stats?user_id=${userId}&days=${days}`
  );
  return response.json();
};
```

### 데이터 형식

#### 자세 기록 요청 형식

```json
{
  "neck_angle": 15.5,
  "shoulder_slope": 2.3,
  "head_forward": 45.2,
  "shoulder_height_diff": 5.1,
  "score": 85.0,
  "cervical_lordosis": 12.3,
  "forward_head_distance": 85.0,
  "head_tilt": 3.2,
  "left_shoulder_height_diff": 4.8,
  "left_scapular_winging": 2.1,
  "right_scapular_winging": 1.9,
  "shoulder_forward_movement": 15.3,
  "session_id": "session_123",
  "device_info": "Chrome/Windows"
}
```

#### 자세 통계 응답 형식

```json
{
  "total_records": 150,
  "average_score": 82.5,
  "improvement_rate": 15.2,
  "normal_posture_rate": 68.3,
  "last_measurement": "2024-01-15T10:30:00"
}
```

## 🔍 문제 해결

### 일반적인 문제

#### 1. Docker 연결 오류

```bash
# Docker Desktop 실행 확인
docker --version

# 컨테이너 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs backend
```

#### 2. 데이터베이스 연결 오류

```bash
# 데이터베이스 컨테이너 상태 확인
docker-compose logs db

# 데이터베이스 직접 연결 테스트
docker-compose exec db mysql -u user -p testdb
```

#### 3. 포트 충돌

```bash
# 포트 사용 확인
netstat -an | findstr :8000  # Windows
lsof -i :8000               # macOS/Linux

# 다른 포트로 변경
# docker-compose.yml에서 ports 섹션 수정
```

## 📄 라이선스

MIT License

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.

---

**Posture Check App Backend** - 건강한 자세를 위한 스마트한 솔루션 🎯
