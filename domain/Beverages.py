# domain/Beverages.py
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, condecimal, field_validator, ConfigDict
from sqlalchemy import Integer, String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from database.db import Base

class Beverage(Base):
    __tablename__ = "beverages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    volume: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class BeverageBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: str = Field(..., min_length=1, max_length=50)
    price: condecimal(max_digits=10, decimal_places=2)
    volume: Optional[str] = Field(None, max_length=20)
    stock_quantity: int = Field(0, ge=0)

    @field_validator("name", "type")
    @classmethod
    def strip_text(cls, v: str) -> str:
        return v.strip()

class BeverageCreate(BeverageBase):
    pass

class BeverageUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    volume: Optional[str] = Field(None, max_length=20)
    stock_quantity: Optional[int] = Field(None, ge=0)

    @field_validator("name", "type")
    @classmethod
    def strip_optional(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v

class BeverageOut(BeverageBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
