# from sqlalchemy.ext.asyncio import:
from database.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from domain.Users import User, UserCreate, UserUpdate, StaffLogin


from fastapi import HTTPException, status, Depends

#CRUD
class UserCrud:
    #get user_id
    @staticmethod
    def get_id( user_id:int, db:Session):    
        result =  db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()
    # def get_id(db:Session, user_id:int):
    #     user_id =  db.query(User).filter(User.user_id == user_id).first()

    #get phone O
    @staticmethod
    def get_phone(phone:str,db:Session):
        result =  db.execute(select(User).where(User.phone == phone))
        return result.scalar_one_or_none()

    #Create O
    @staticmethod
    def create_user(user:UserCreate,db:Session):
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.flush()
        return db_user
    
    #Delete
    @staticmethod
    def delete_user(user_id:int,db:Session):
        db_user = db.get(User, user_id)
        if db_user:
             db.delete(db_user)
             db.flush()
             return db_user
        return None     

    #Update (user_id)
    @staticmethod
    def update_user(user_id:int, user:UserUpdate,db:Session):
        pass

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
        
        try:
            db_user =  UserCrud.create_user(user,db)
            db.commit()
            db.refresh(db_user)
            return db_user

        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="전화번호 또는 비밀번호가 부적절합니다")

        #jwt 인증
        # hash_pw=
        # jwt작성후 password변경
        # user_create=UserCreate(name=user.name,
        #                        phone=user.phone,
        #                        password=hash_pw,
        #                        address=user.address,
        #                        is_staff=user.is_staff)        

    @staticmethod
    def login(user:StaffLogin, db:Session):
        pass
