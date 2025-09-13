from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
# from sqlalchemy.orm import AsyncSession

from sqlalchemy import select
from domain.Users import User, UserCreate, UserUpdate, StaffLogin
from security.Jwt import hash_password, verify_password, create_access_token, create_refresh_token

from fastapi import HTTPException, status, Depends

#CRUD
class UserCrud:
    #get user_id 
    @staticmethod
    async def get_id( user_id:int, db:AsyncSession):    
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()   

    #get phone(username대신 사용) 
    @staticmethod
    async def get_phone(phone:str,db:AsyncSession):
        result = await db.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none()

    #Create 
    @staticmethod
    async def create_user(user:UserCreate,db:AsyncSession)->User:
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.commit()     #commit/ flush 
        await db.refresh(db_user)    
        return db_user
    
    #Delete 
    @staticmethod
    async def delete_user_by_id(user_id:int,db:AsyncSession):
        db_user = await db.get(User, user_id)
        if db_user:
            await db.delete(db_user)
            await db.commit()
            return db_user
        return None     

    #Update (user_id)
    @staticmethod
    async def update_user_by_id(user:UserUpdate, user_id:int, db:AsyncSession):
        db_user = await db.get(User, user_id)
        if db_user:
            update_user = user.model_dump(exclude_unset=True)
            for name, value in update_user.items():
                #업데이트시 비밀번호 노출방지
                if name =="password":
                    value = await hash_password(value)
                setattr(db_user,name,value)
            await db.commit()     #commit/ flush 
            await db.refresh(db_user)             
            return db_user
        return None

    #jwt 인증관련
    #refresh_token
    @staticmethod
    async def update_refresh_token(
        user_id:int,refresh_token:str, db:AsyncSession) ->User:
        db_user = await db.get(User, user_id)        
        if db_user:
            db_user.refresh_token = refresh_token
            await db.flush()
        return db_user

#Service
class UserService:
    #signup 기본기능 -> is_staff -> 직원만 로그인        
    # 로그인 시 is_staff 확인 → JWT 발급
    #DB에서 id의 사용자 조회
    @staticmethod
    async def get_user(user_id:int, db:AsyncSession) -> User:
        db_user = await UserCrud.get_id(user_id,db)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="사용자 없음")
        return db_user

    @staticmethod
    async def signup(user:UserCreate,db:AsyncSession) ->User:
        # 중복 phone확인
        if await UserCrud.get_phone(user.phone,db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,        
                                detail="이미 가입한 번호입니다")   
        #비밀번호 해싱     
        hashed_pw= await hash_password(user.password)
        #유저객체
        user_create = UserCreate(name=user.name,
                                phone=user.phone,
                                password=hashed_pw,
                                address=user.address,
                                is_staff=user.is_staff                        
                                )
        try:                
            #DB저장
            db_user = await UserCrud.create_user(user_create,db)              
            return db_user

        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="전화번호 또는 비밀번호가 부적절합니다")
                 
    # login  (username: phone, password:password 사용) / 
    # 직원만(is_staff=True)로그인가능
    @staticmethod
    async def login(user:StaffLogin, db:AsyncSession)-> tuple[User,str,str]:
        db_user = await UserCrud.get_phone(user.phone,db)
        
        if not db_user or not await verify_password(user.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="잘못된 사용자 혹은 비밀번호입니다")
        #직원여부 확인
        if not db_user.is_staff:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="직원만 로그인 가능합니다")
        
        #jwt token 
        access_token = create_access_token(db_user.user_id)   
        refresh_token = create_refresh_token(db_user.user_id)

        verified_staff= await UserCrud.update_refresh_token(db_user.user_id,
                                                            refresh_token,db)
        await db.commit()
        await db.refresh(verified_staff)
        return verified_staff, access_token, refresh_token

        
