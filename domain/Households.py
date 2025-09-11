from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from typing import Optional

Base = declarative_base()

class HouseHolds(Base):

    __tablename__="households"

    h_id = Column(Integer, primary_key=True)
    h_name = Column(String(50), unique=True, nullable=False)
    h_price = Column(Integer,nullable=False)
    h_description = Column(String(300), nullable=False)
    h_quantity = Column(Integer, nullable=False)

class HouseHoldCreate(BaseModel):    
    h_name: str = Field(..., min_length=1)    
    h_price: int = Field(..., ge=0)
    h_description: str = Field(..., min_length=1)
    h_quantity: int = Field(..., ge=1)

class HouseHoldUpdate(BaseModel):
    h_name: Optional[str] = None
    h_price: Optional[int] = None
    h_description: Optional[str] = None
    h_quantity: Optional[int] = None

class HouseHoldResponse(BaseModel):
    h_id: int
    h_name: str
    h_price: int
    h_description: str
    h_quantity: int
    
    class Config:
        from_attributes = True