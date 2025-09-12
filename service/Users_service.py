# from sqlalchemy.ext.asyncio import:
from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from domain.Users import User, UserCreate, UserUpdate, StaffLogin
from security.Jwt import hash_password, verify_password, create_access_token, create_refresh_token

from fastapi import HTTPException, status, Depends

#CRUD
class UserCrud:
    #get user_id 
    @staticmethod
    def get_id( user_id:int, db:Session):    
        result =  db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()   

    #get phone 
    @staticmethod
    def get_phone(phone:str,db:Session):
        result =  db.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none()

    #Create 
    @staticmethod
    def create_user(user:UserCreate,db:Session)->User:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()     #commit/ flush 
        db.refresh(db_user)    
        return db_user
    
    #Delete 
    @staticmethod
    def delete_user_by_id(user_id:int,db:Session):
        db_user = db.get(User, user_id)
        if db_user:
             db.delete(db_user)
             db.commit()
             return db_user
        return None     

    #Update (user_id)
    @staticmethod
    def update_user_by_id(user_id:int, user:UserUpdate,db:Session):
        db_user = db.get(User, user_id)
        if db_user:
            update_user = user.model_dump(exclude_unset=True)
            for name, value in update_user.items():
                setattr(db_user,name,value)
            db.commit()     #commit/ flush 
            db.refresh(db_user)             
            return db_user
        return None

    #jwt 인증관련
    #refresh_token
    @staticmethod
    async def update_refresh_token(user_id:int,refresh_token:str, db:Session):
        db_user = db.get(User, user_id)        
        if db_user:
            db_user.refresh_token

#Service
class UserService:
    #signup 기본기능 -> is_staff -> 직원만 로그인
    # 손님이면 phone[-4:] 비번 자동 생성
    # 직원이면 password 필수 + 해시
    # 로그인 시 is_staff 확인 → JWT 발급
    @staticmethod
    def signup(user:UserCreate,db:Session):
        # 중복 phone확인
        if  UserCrud.get_phone(user.phone,db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,        
                                detail="이미 가입한 번호입니다")   
        #비밀번호 해싱     
        hashed_pw= hash_password(user.password)
        #유저객체
        user_create = UserCreate(name=user.name,
                                phone=user.phone,
                                password=hashed_pw,
                                address=user.address,
                                is_staff=user.is_staff                        
                                )
        try:                
            #DB저장
            db_user = UserCrud.create_user(user_create,db)              
            return db_user

        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="전화번호 또는 비밀번호가 부적절합니다")
                 
    # phone =(email), password= password
    @staticmethod
    def login(user:StaffLogin, db:Session):
        db_user = UserCrud.get_phone(user.phone,db)
        if not db_user or not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="잘못된 사용자 혹은 비밀번호입니다")
        
        access_token = create_access_token(db_user.user_id)   
        refresh_token = create_refresh_token(db_user.user_id)

        
