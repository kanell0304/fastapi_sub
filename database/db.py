from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ DATABASE_URL 우선순위: 환경변수 > .env (uvicorn --env-file .env 로 로드 가능)
# 예) MySQL:  mysql+pymysql://user:password@localhost:3306/fastapi_db?charset=utf8mb4
# 예) SQLite: sqlite:///./app.db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Engine & Session
engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# SQLAlchemy Base
Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
