from pydantic import BaseModel, Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from typing import Optional
from database.db import engine, Base

#ORM
class Snack(Base):
    
    __tablename__="snacks"

    s_id: Mapped[int] = mapped_column(primary_key=True)
    s_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    s_price: Mapped[int] = mapped_column(nullable=False)    
    s_quantity: Mapped[int] = mapped_column(nullable=False)
    s_exp_date: Mapped[date] = mapped_column(nullable=False)
    s_description: Mapped[str | None] = mapped_column(String(300), nullable=True)

# Base.metadata.create_all(bind=engine) 09.12 19:48 주석처리


#pydantic모델 공통 필드
class SnackBase(BaseModel):
    s_name: str=Field(..., max_length=50, title="상품 이름")
    s_price: int=Field(..., ge=0, title="가격")
    s_quantity: int=Field(0, ge=0, title="재고 수량")
    s_exp_date: date=Field(..., title="유통기한")
    s_description: Optional[str]=Field(None, title="상세정보")

#등록
class CreateSnack(SnackBase):
    pass

#R
class ReadSnack(SnackBase):
    s_id: int

#수정
class UpdateSnack(BaseModel):
    s_name: Optional[str]=Field(None, max_length=50, title="상품 이름")
    s_price: Optional[int]=Field(None, ge=0, title="가격")
    s_quantity: Optional[int]=Field(None, ge=0, title="재고 수량")
    s_exp_date: Optional[date]=Field(None, title="유통기한")
    s_description: Optional[str]=Field(None, title="상세정보")    

#DB에 저장된 상품 정보
class SnackInDB(SnackBase):
    s_id: int

    class Config:
        from_attributes=True