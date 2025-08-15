"""
Posture Check App Backend - 데이터베이스 모델 패키지

이 패키지는 애플리케이션의 모든 데이터베이스 모델을 정의합니다.

포함된 모델:
- User: 사용자 계정 정보
- PostureRecord: 자세 측정 기록 (13개 지표)
- PostureSession: 자세 측정 세션 관리
- PostureAnalysis: 자세 분석 결과

모든 모델은 SQLAlchemy ORM을 사용하여 정의되며,
데이터베이스 테이블과 자동으로 매핑됩니다.
""" 