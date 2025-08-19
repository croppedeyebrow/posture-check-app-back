#!/usr/bin/env python3
"""
Posture Check App Backend - WSGI Entry Point

Render 배포를 위한 WSGI 진입점
"""

import os
import sys

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# FastAPI 앱 import
from app.main import app

# WSGI 애플리케이션
application = app
