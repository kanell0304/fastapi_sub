from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from domain.Users import User, UserCreate, UserUpdate,StaffLogin,UserRead
from service.Users_service import UserService, UserCrud

router = APIRouter()

prefix="/users"

#회원가입 
@router.post("/signup", response_model= UserRead)
async def signup(user:UserCreate,db:AsyncSession=Depends(get_db)):
    db_user = await UserService.signup(user,db)
    return db_user

#user_id조회
@router.get("/userme", response_model=UserRead)
async def get_user(user_id:int, db:AsyncSession=Depends(get_db)):
    return await UserCrud.get_id(user_id,db)

#회원삭제
@router.delete("/delete/{user_id}")
async def delete_user(user_id:int,db:AsyncSession=Depends(get_db)):
    result = await UserCrud.delete_user_by_id(user_id,db)
    return {"msg":"회원삭제","deleted":result}

#회원정보수정   
@router.put("/update/{user_id}")
async def update_user_by_id(user_id:int, user:UserUpdate,db:AsyncSession=Depends(get_db)):
    result = await UserCrud.update_user_by_id(user_id,user,db)    
    return result
