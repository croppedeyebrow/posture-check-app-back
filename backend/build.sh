#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# 데이터베이스 마이그레이션 (필요한 경우)
# python -m alembic upgrade head
