#!/bin/bash

# Railway 배포 스크립트
echo "🚀 Railway 배포 시작..."

# Railway CLI 설치 확인
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI가 설치되지 않았습니다."
    echo "설치 방법: npm install -g @railway/cli"
    exit 1
fi

# 로그인 확인
if ! railway whoami &> /dev/null; then
    echo "🔐 Railway에 로그인하세요..."
    railway login
fi

# 프로젝트 배포
echo "📦 프로젝트 배포 중..."
railway up

echo "✅ 배포 완료!"
echo "🌐 배포된 URL을 확인하려면: railway status"
