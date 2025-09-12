# database/db.py
from __future__ import annotations

import os, asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db")

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db

# ✅ 최초 기동 시 테이블 생성 (학습/과제용)
async def init_models():
    from domain.Beverages import Beverage  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 모듈 import 시 1회 실행 (uvicorn --reload 환경에서도 안전)
try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(init_models())
    else:
        loop.run_until_complete(init_models())
except RuntimeError:
    asyncio.run(init_models())
