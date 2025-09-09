from pydantic import BaseModel, Field, EmailStr
# from database.database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base
from typing import Optional, Annotated

#db 연결후 삭제
Base = declarative_base()

class User(Base):
    __tablename__="users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(40), nullable=False)
    email = Column(String(100),nullable=False)    
    password = Column(String(100), nullable=False)
    address = Column(String(300), nullable=False)

class UserCreate(BaseModel):    
    username:str = Field(...,min_length=2)    
    email = EmailStr
    password:str = Field(...,min_length=3, max_length=20)
    address:str = Field(...)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    address: Optional[str] = None


class UserLogin(BaseModel):
    username:str|None = None
    password:str|None = None



