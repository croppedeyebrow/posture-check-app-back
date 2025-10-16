# 🧍‍♂️ Posture Check App Backend  
> **실시간 자세 분석 및 교정 피드백을 위한 FastAPI 기반 백엔드 서버**

[🔗 Frontend Repository](https://github.com/croppedeyebrow/posture-check-app)

---

## 🩺 프로젝트 개요 

> 자세 데이터를 실시간으로 수집·분석하여  
> 의학적 기준에 따라 정상/비정상 자세를 판별하고  
> 사용자별 개선 추이를 시각화하는 **의료 데이터 기반 헬스케어 백엔드 서비스**입니다.

핵심 특징
의학적 정확성: 실제 의료 기준을 반영한 자세 분석
13개 자세 지표: 포괄적인 자세 측정 및 분석
실시간 처리: 실시간 자세 감지 및 피드백
데이터 분석: 통계 및 트렌드 분석 기능
확장 가능한 구조: 모듈화된 아키텍처

| 항목 | 내용 |
|------|------|
| 🧠 목적 | 실시간 자세 분석 및 피드백 제공 |
| ⚙️ 기술 스택 | **FastAPI**, **SQLAlchemy**, **MySQL**, **Pydantic**, **Alembic** |
| 📊 분석 지표 | 13개 자세 지표 (목각도, 어깨기울기 등) |
| 🧩 아키텍처 | RESTful API, ORM 기반 계층화 구조 |
| 🔗 연동 | React 기반 프론트엔드와 완전 연동 (CORS 설정 완료) |




---

## 🚀 주요 기능
1. 자세 기록 관리
13개 자세 지표 저장 및 조회
세션 기반 데이터 관리
날짜별 필터링 및 검색 기능
2. 실시간 자세 분석
의학적 기준 기반 자세 판단
정상/비정상 자동 분류
개선 제안 및 피드백 제공
3. 통계 및 트렌드 분석
개선률 계산: 기간별 자세 개선 추이
정상 자세 비율: 전체 측정 대비 정상 자세 비율
일별 트렌드: 시간에 따른 자세 변화 패턴
4. 의학적 정확성
목 각도: -30° ~ 30° (정상 범위)
전방 머리 거리: ≤ 100mm (최대 정상값)
머리 기울기: -15° ~ 15° (정상 범위)
---

## 🧬 데이터 지표 (13개)

| 구분 | 필드명 | 설명 | 단위 |
|------|---------|------|------|
| ✅ 기본 | neck_angle | 목 각도 | ° |
|  | shoulder_slope | 어깨 기울기 | ° |
|  | head_forward | 머리 전방 이동 | mm |
|  | shoulder_height_diff | 어깨 높이 차이 | mm |
|  | score | 종합 점수 | 점 |
| 🩻 확장 | cervical_lordosis | 경추 전만각 | ° |
|  | forward_head_distance | 전방 머리 거리 | mm |
|  | head_tilt | 머리 기울기 | ° |
|  | left_shoulder_height_diff | 왼쪽 어깨 높이 차이 | mm |
|  | scapular_winging_left/right | 견갑골 돌출 정도 | mm |
|  | shoulder_forward_movement | 어깨 전방 이동 | mm |



---

## 🏗 기술 스택

| 구분 | 기술 |
|------|------|
| **Framework** | FastAPI, SQLAlchemy, Pydantic |
| **Database** | MySQL 8.0, Alembic |
| **Infra** | Docker, Docker Compose |
| **Language** | Python 3.11 |
| **Server** | Uvicorn (ASGI) |

---

## 📁 프로젝트 구조

posture_app_back/
├── backend/
│ ├── app/
│ │ ├── main.py # FastAPI 엔트리포인트
│ │ ├── core/ # 설정 및 환경변수 관리
│ │ ├── db/ # DB 연결 및 세션 관리
│ │ ├── models/ # SQLAlchemy 모델
│ │ ├── schemas/ # Pydantic 스키마 정의
│ │ ├── crud/ # CRUD 비즈니스 로직
│ │ ├── api/v1/endpoints/ # API 라우팅
│ │ └── tests/ # 단위 테스트
│ ├── requirements.txt
│ └── Dockerfile
├── docker-compose.yml
└── README.md

---

## 🧠 설계 포인트

| 핵심 영역 | 설명 |
|------------|------|
| **의학적 근거 기반 설계** | 의료 논문 기준으로 정상범위(예: 목 각도 -30°~30°) 설정 |
| **데이터 일관성 보장** | ORM + Pydantic을 통한 요청/응답 검증 |
| **확장 가능한 구조** | API 버전 관리(`/api/v1/`), 모듈화된 CRUD 구조 |
| **비동기 처리** | Uvicorn 기반 ASGI로 실시간 요청 처리 |
| **보안 설계(예정)** | JWT 기반 사용자 인증 추가 예정 |

---

📍Swagger 문서: http://localhost:8000/docs

📍ReDoc 문서: http://localhost:8000/redoc

---


## 🔍 주요 API 엔드포인트

| Method | Endpoint                            | 설명       |
| ------ | ----------------------------------- | -------- |
| `POST` | `/api/v1/posture/record`            | 자세 기록 생성 |
| `GET`  | `/api/v1/posture/records`           | 전체 기록 조회 |
| `GET`  | `/api/v1/posture/stats`             | 통계 조회    |
| `POST` | `/api/v1/posture/analyze`           | 실시간 분석   |
| `GET`  | `/api/v1/posture/medical-standards` | 의료 기준 조회 |

---

## 📊 데이터베이스 개요

| 테이블                | 설명            |
| ------------------ | ------------- |
| `users`            | 사용자 기본 정보     |
| `posture_records`  | 자세 측정값 저장 테이블 |
| `posture_sessions` | 세션별 자세 데이터 구분 |
| `posture_analyses` | 분석 결과 기록      |


## 🧩 아키텍처 구조

- 클라이언트: React 

- API 서버: FastAPI

- DB: MySQL

- ORM: SQLAlchemy

- 마이그레이션: Alembic

- 실시간 분석 모듈: Python 로직 (자세 지표 계산)

---

## 🏗️ 자세 교정 앱 백엔드 아키텍처

### 1. POST 요청 흐름 (자세 기록 및 실시간 분석)
```
클라이언트 (App)
    ↓ (POST /api/v1/posture/record)
FastAPI 엔드포인트 (posture.py)
    ↓ (데이터 바인딩 및 의존성 주입)
Pydantic 데이터 검증 (PostureRecordCreate 스키마)
    ↓ (유효성 검증 성공)
핵심 비즈니스 로직 (CRUD 레이어)
    ↓
실시간 분석 모듈 실행 (의학적 기준 기반)
    ↓
CRUD 처리 (SQLAlchemy ORM)
    ↓
MySQL (posture_records 테이블에 데이터 저장)
    ↓ (저장된 데이터를 Pydantic Read 스키마로 직렬화)
FastAPI 엔드포인트
    ↓ (HTTP 200 OK 응답)
클라이언트 (App)
```

### 2. GET 요청 흐름 (통계 및 트렌드 조회)

```
클라이언트 (App)
    ↓ (GET /api/v1/posture/stats?user_id=N&days=D)
FastAPI 엔드포인트 (posture.py)
    ↓ (Query Parameter 수신)
CRUD 처리 (SQLAlchemy ORM)
    ↓ (기간별 자세 기록 데이터 조회)
MySQL (posture_records)
    ↓ (조회된 데이터 반환)
CRUD 레이어 (통계 계산 로직)
    ↓ (개선률, 정상 자세 비율 등 계산)
Pydantic 데이터 직렬화 (PostureStatsResponse 스키마)
    ↓
FastAPI 엔드포인트
    ↓ (HTTP 200 OK 응답)
클라이언트 (App)
```



---

## 📡 API 구조
```
- /api/v1/posture/record → POST → 자세 기록 저장

- /api/v1/posture/records → GET → 기록 조회

- /api/v1/posture/stats → GET → 통계 조회

- /api/v1/posture/trends → GET → 트렌드 조회

- /api/v1/posture/analyze → POST → 실시간 분석

- /api/v1/posture/medical-standards → GET → 의학적 기준 조회

- /health → GET → 헬스 체크

```
---

## 🗃 ERD 구조


## 💾 상세 $\text{ERD}$ 구조 (표 형식)

| 엔티티 (테이블) | 속성 (컬럼) | 키 및 관계 | 비고 |
| :--- | :--- | :--- | :--- |
| **USERS** | `id`, `username`, `email`, `hashed_password`, `is_active` | `id` **(PK)** | 서비스의 최상위 사용자 정보 |
| **POSTURE\_SESSIONS** | `id`, `user_id`, `session_id`, `start_time`, `end_time`, `total_records`, `average_score` | `id` **(PK)**, `user_id` **(FK)** ($\to \text{USERS}$) | 측정 세션 단위로 데이터 집계 및 관리 |
| **POSTURE\_RECORDS** | `id`, `user_id`, `neck_angle`, `shoulder_slope` $\dots$ ($\text{13}$개 지표), `session_id`, `device_info` | `id` **(PK)**, `user_id` **(FK)** ($\to \text{USERS}$), `session_id` **(FK)** ($\to \text{POSTURE\_SESSIONS}$) | 개별 측정 시점의 $\text{Raw Data}$ 기록 ($\text{13}$개 지표) |
| **POSTURE\_ANALYSIS** | `id`, `user_id`, `session_id`, `problem_description`, `solution_suggestion`, `severity_level`, `deviation` | `id` **(PK)**, `user_id` **(FK)** ($\to \text{USERS}$), `session_id` **(FK)** ($\to \text{POSTURE\_SESSIONS}$) | 세션 기반의 최종 분석 해석 결과 저장 |

### 엔티티 간 관계 요약

| 관계 $\text{From}$ | 관계 유형 | 관계 $\text{To}$ | 설명 |
| :--- | :--- | :--- | :--- |
| **USERS** | $\text{1:N}$ (일대다) | **POSTURE\_SESSIONS** | 한 명의 사용자는 여러 세션을 가질 수 있음 |
| **USERS** | $\text{1:N}$ (일대다) | **POSTURE\_RECORDS** | 한 명의 사용자는 여러 자세 기록을 가질 수 있음 |
| **POSTURE\_SESSIONS** | $\text{1:N}$ (일대다) | **POSTURE\_RECORDS** | 하나의 세션에 여러 개의 개별 자세 기록이 포함됨 |
| **POSTURE\_SESSIONS** | $\text{1:1}$ (일대일) | **POSTURE\_ANALYSIS** | 하나의 세션에 하나의 최종 분석 결과가 도출됨 (혹은 $\text{1:N}$으로 확장 가능) |


---

## 🔄 플로우차트

클라이언트 요청 (POST/GET)

FastAPI 엔드포인트

Pydantic 데이터 검증

CRUD 처리 (SQLAlchemy → MySQL)

실시간 분석 모듈 실행 (POST 요청 시)

결과 반환 → 클라이언트 표시


---




