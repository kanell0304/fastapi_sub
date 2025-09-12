from fastapi import APIRouter, Depends, Response,Request
from fastapi import HTTPException, status

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from domain.Users import User, UserCreate, UserUpdate,StaffLogin,UserRead,AuthResponse,PrivateUserRead
from service.Users_service import UserService, UserCrud

router = APIRouter()

prefix="/users"

#회원가입 (Create)
@router.post("/signup", response_model= UserRead)
async def signup(user:UserCreate,db:AsyncSession=Depends(get_db)):
    db_user = await UserService.signup(user,db)
    return db_user

#이름조회 -모든유저(Read)
@router.get("/name/{user_id}", response_model=UserRead)
async def get_name(user_id:int, db:AsyncSession=Depends(get_db)):
    return await UserCrud.get_id(user_id,db)

#회원삭제 (Delete)
@router.delete("/delete/{user_id}")
async def delete_user(user_id:int,db:AsyncSession=Depends(get_db)):
    result = await UserCrud.delete_user_by_id(user_id,db)
    return {"msg":"회원삭제","deleted":result}

#회원정보수정 (Update)
@router.put("/update/{user_id}")
async def update_user_by_id(user_id:int, user:UserUpdate,db:AsyncSession=Depends(get_db)):
    result = await UserCrud.update_user_by_id(user_id,user,db)    
    return result

#로그인 (JWT token생성 header/bearer)
@router.post("/login", response_model=AuthResponse)
async def login(staff:StaffLogin, db:AsyncSession=Depends(get_db)):
    result = await UserService.login(staff,db)
    verified_staff, access_token, refresh_token = result
    return {
        "verified_staff":verified_staff,
        "access_token":access_token,
        "refresh_token":refresh_token
    }
    # 쿠키방식 변경 
    # set_cookies(verified_staff,access_token,refresh_token)
    # return db_user

# 로그인한 직원만 사용자 상세 정보 조회
# jwt verify
# @router.get("/manage/{user_id}", response_model=PrivateUserRead)
# async def get_user(request:Request ,db:AsyncSession=Depends(get_db)):
#     pass



