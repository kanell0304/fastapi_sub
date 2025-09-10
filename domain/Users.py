from pydantic import BaseModel, Field, field_validator, ValidationError
# from database.database import Base
from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, String, Integer, Boolean
from typing import Optional, Annotated

#db 연결후 삭제
Base = declarative_base()

#전화번호,이름, 4자리, 인증 암호화부분

class User(Base):
    __tablename__="users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(40), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(100), nullable=False)
    address = Column(String(300), nullable=False)
    
    admin = Column(Boolean, default=False)
    admin_pw = Column(String(100), nullable=False)

class UserCreate(BaseModel):    
    username:str = Field(...,min_length=2)    
    phone:str = Field(...,min_length=4, max_length=20, description="'-'제외")
    password:str = Annotated[Field(...,min_length=3, max_length=4),phone[-4:]] ###전화번호 맨뒤 4자리
    address:str = Field(...)
    admin:bool | None = False   





class UserUpdate(BaseModel):
    username:Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    admin: Optional[bool] = False

#admin
class AdminLogin(BaseModel):
    username:str|None = None
    admin_pw:str|None = None
    address:str|None = None
    admin: bool = False

