from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session
from sqlalchemy import select
from domain.Users import User, UserCreate, UserUpdate, UserLogin
from pydantic import EmailStr

class UserCrud:
    #
    @staticmethod
    async def get_id(db:AsyncSession, user_id:int):    
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none
    # async def get_id(db:Session, user_id:int):
    #     user_id = await db.query(User).filter(User.user_id == user_id).first()

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

    #get_email
    @staticmethod
    async def get_username(db:AsyncSession, username:str):
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    #Update
    @staticmethod
    async def update_user(db:AsyncSession, user_id:int, user:UserUpdate):
        pass


class UserService:
    @staticmethod
    async def signup(db:AsyncSession,user:UserCreate):
        pass
    @staticmethod
    async def login(db:AsyncSession,user:UserLogin):
        pass
