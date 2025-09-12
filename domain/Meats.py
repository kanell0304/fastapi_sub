from pydantic import BaseModel, Field
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from typing import Optional
from database.db import engine, Base

#ORM
class Meat(Base):

    __tablename__="meats"
    # (id와 상세정보를 제외한) 모든 값이 동일한 상품의 등록 막는 제약조건
    __table_args__ = (UniqueConstraint('m_animal', 'm_part', 'm_country',
                    'm_weight', 'm_price', 'm_prep_date', name='uniqueConstraint_meats'), )
    

    m_id: Mapped[int] = mapped_column(primary_key=True)
    m_animal: Mapped[str] = mapped_column(String(20), nullable=False)
    m_part: Mapped[str] = mapped_column(String(50), nullable=False)
    m_country: Mapped[str] = mapped_column(String(50), nullable=False)
    m_weight: Mapped[int] = mapped_column(nullable=False)
    m_price: Mapped[int] = mapped_column(nullable=False)    
    m_prep_date: Mapped[datetime] = mapped_column(nullable=False)
    m_description: Mapped[str | None] = mapped_column(String(300), nullable=True)

# Base.metadata.create_all(bind=engine) 09.12 19:48 주석처리



#pydantic모델 공통 필드
class MeatBase(BaseModel):
    m_animal: str=Field(..., max_length=20, title="품종")
    m_part: str=Field(..., max_length=50, title="부위")
    m_country: str=Field(..., max_length=50, title="원산지")
    m_weight: int=Field(..., gt=0, title="그람수")
    m_price: int=Field(..., ge=0, title="가격")
    m_prep_date: datetime=Field(default_factory=lambda : datetime.now(timezone.utc), title="도축일자") 
    m_description: Optional[str]=Field(None, title="상세정보")

#등록
class CreateMeat(MeatBase):
    pass

#R
class ReadMeat(MeatBase):
    m_id: int

#수정
class UpdateMeat(BaseModel):
    m_animal: Optional[str]=Field(None, max_length=20, title="품종")
    m_part: Optional[str]=Field(None, max_length=50, title="부위")
    m_country: Optional[str]=Field(None, max_length=50, title="원산지")
    m_weight: Optional[int]=Field(None, gt=0, title="그람수")
    m_price: Optional[int]=Field(None, ge=0, title="가격")
    m_prep_date: Optional[datetime]=Field(None, title="도축일자") 
    m_description: Optional[str]=Field(None, title="상세정보")    

#DB에 저장된 고기 정보
class MeatInDB(MeatBase):
    m_id: int

    class Config:
        from_attributes=True