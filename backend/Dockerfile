FROM python:3.11-slim

WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python 환경 최적화
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 의존성 파일만 먼저 복사 (캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드는 볼륨 마운트로 처리하므로 복사하지 않음
# COPY ./app ./app

# 헬스체크를 위한 대기 스크립트 추가
RUN echo '#!/bin/bash\n\
echo "Waiting for application to be ready..."\n\
until curl -f http://localhost:8000/health; do\n\
  echo "Application not ready yet. Waiting..."\n\
  sleep 2\n\
done\n\
echo "Application is ready!"' > /app/wait-for-app.sh && chmod +x /app/wait-for-app.sh

# 애플리케이션 디렉토리 생성
RUN mkdir -p /app/app

EXPOSE 8000

# 기본 명령어 (docker-compose에서 override됨)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
