from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.db import get_db
from domain.Users import User, UserCreate, UserUpdate,StaffLogin,UserRead
from service.Users_service import UserService, UserCrud

router = APIRouter()

prefix="/users"

#회원가입 
@router.post("/signup", response_model= UserRead)
def signup(user:UserCreate,db:Session=Depends(get_db)):
    db_user = UserService.signup(user,db)
    return db_user

#user_id조회
@router.get("/userme", response_model=UserRead)
def get_user(user_id:int, db:Session=Depends(get_db)):
    return UserCrud.get_id(user_id,db)

#회원삭제
@router.delete("/delete/{user_id}")
def delete_user(user_id:int,db:Session=Depends(get_db)):
    result = UserCrud.delete_user_by_id(user_id,db)
    return {"msg":"회원삭제","deleted":result}

#회원정보수정   
@router.put("/update/{user_id}")
def update_user_by_id(user_id:int, user:UserUpdate,db:Session=Depends(get_db)):
    result = UserCrud.update_user_by_id(user_id,user,db)    
    return result
