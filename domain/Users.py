from pydantic import BaseModel, Field, field_validator, ValidationError
# from database.database import Base
from sqlalchemy.orm import declarative_base

from sqlalchemy import Column, String, Integer, Boolean
from typing import Optional, Annotated

#db 연결후 삭제
Base = declarative_base()

#전화번호,이름, 4자리, 인증 암호화부분
#SQLalchemy
class User(Base):
    __tablename__="users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    phone = Column(String(20), unique=True,nullable=False)
    password = Column(String(100))
    address = Column(String(300), nullable=False)    
    is_staff = Column(Boolean, default=False, nullable=False)

#pydantic Create 
class UserCreate(BaseModel):    
    name:str = Field(...,min_length=2)    
    phone:str = Field(...,min_length=4, max_length=30)
    password:str|None = Field(None,min_length=4, max_length=50) #손님-전화번호4자리/직원-비밀번호
    address:str = Field(...)
    is_staff:bool | None = False  

#pydantic Update
class UserUpdate(BaseModel):
    name:Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None
    is_staff: Optional[bool] = None

#login-직원만 전화번호/비밀번호
class StaffLogin(BaseModel):    
    phone:str|None = None
    password:str|None = None    

#pydantic Read 
class UserRead(BaseModel):
    user_id: int
    name: str
    phone: str
    address: str
    is_staff: bool

    #ORM -> pydantic mapping (ORM 객체 속성을 읽어 Pydantic 필드로 매핑 가능하게 함)
    class Config:
        from_attributes = True