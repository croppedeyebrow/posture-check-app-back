FROM python:3.11-slim

WORKDIR /app

# 시스템 패키지 업데이트 및 curl 설치
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 의존성 파일만 먼저 복사 (캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드는 볼륨 마운트로 처리하므로 복사하지 않음
# COPY ./app ./app

# 헬스체크를 위한 대기 스크립트 추가
RUN echo '#!/bin/bash\n\
until curl -f http://localhost:8000/health; do\n\
  echo "Waiting for application to be ready..."\n\
  sleep 2\n\
done' > /app/wait-for-app.sh && chmod +x /app/wait-for-app.sh

EXPOSE 8000

# 기본 명령어 (docker-compose에서 override됨)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
