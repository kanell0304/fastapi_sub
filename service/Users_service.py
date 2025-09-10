from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session
from sqlalchemy import select
from domain.Users import User, UserCreate, UserUpdate, UserLogin
from pydantic import EmailStr
from fastapi import HTTPException, status

#CRUD
class UserCrud:
    #get user_id
    @staticmethod
    async def get_id(db:AsyncSession, user_id:int):    
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none
    # async def get_id(db:Session, user_id:int):
    #     user_id = await db.query(User).filter(User.user_id == user_id).first()

    #get phone
    @staticmethod
    async def get_phone(db:AsyncSession, phone:str):
        result = await db.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none

    #Create
    @staticmethod
    async def create_user(db:AsyncSession, user:UserCreate):
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.flush()
        return db_user
    #Delete
    @staticmethod
    async def delete_user(db:AsyncSession, user_id:int):
        db_user =await db.get(User, user_id)
        if db_user:
            await db.delete(db_user)
            await db.flush()
            return db_user
        return None     

    #Update (user_id)
    @staticmethod
    async def update_user(db:AsyncSession, user_id:int, user:UserUpdate):
        pass

#Service
class UserService:
    #signup 기본기능 -> is_staff -> 직원만 로그인
    # 손님이면 phone[-4:] 비번 자동 생성
    # 직원이면 password 필수 + 해시
    # 로그인 시 is_staff 확인 → JWT 발급
    @staticmethod
    async def signup(db:AsyncSession,user:UserCreate):
        #중복 phone확인
        if await UserCrud.get_phone(db, user.phone):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="이미 가입한 번호입니다")
        
        #jwt 인증
        # hash_pw=
        # jwt작성후 password변경
        # user_create=UserCreate(name=user.name,
        #                        phone=user.phone,
        #                        password=hash_pw,
        #                        address=user.address,
        #                        is_staff=user.is_staff)
        
        try:
            db_user = await UserCrud.create_user(db,user)
            await db.commit()
            await db.refresh(db_user)
            return db_user

        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="전화번호 또는 비밀번호가 부적절합니다")


    @staticmethod
    async def login(db:AsyncSession,user:UserLogin):
        pass
