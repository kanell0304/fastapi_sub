from fastapi import APIRouter, Depends, Response, Request, HTTPException,status

from sqlalchemy.ext.asyncio import AsyncSession

from security.cookie import set_cookies, get_user_id, refresh_expired_token
from database.db import get_db
from domain.Users import User, UserCreate, UserUpdate,StaffLogin,UserRead,AuthResponse,PrivateUserRead
from service.Users_service import UserService, UserCrud

router = APIRouter()

prefix="/users"


#회원가입 (Create)
@router.post("/signup", response_model= PrivateUserRead)
async def signup(user:UserCreate,db:AsyncSession=Depends(get_db)) -> User:
    db_user = await UserService.signup(user,db)
    return db_user
#이름조회 -모든유저(Read)
@router.get("/name/{user_id}", response_model=UserRead)
async def get_name(user_id:int, db:AsyncSession=Depends(get_db)) ->User:
    user = await UserCrud.get_id(user_id,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="없는 회원")
    return user    

#로그인 (JWT token생성 response객체로 cookie저장)
@router.post("/login", response_model=AuthResponse)
async def login(staff:StaffLogin, response:Response,db:AsyncSession=Depends(get_db)) -> AuthResponse:
    result = await UserService.login(staff,db)
    verified_staff, access_token, refresh_token = result    
    set_cookies(response, access_token, refresh_token)
    return AuthResponse(verified_staff=verified_staff ,access_token=access_token, refresh_token=refresh_token)

#로그인 갱신 (토큰연장, refresh token생성)
@router.post("/refresh", description="로그인 갱신")
async def refresh(request:Request, 
                  response:Response, 
                  db:AsyncSession=Depends(get_db)):
    return await refresh_expired_token(request,response,db)

# 로그인한 직원만 사용자 상세 정보 조회 cookies.get_user_id
# 직원 권한 인증 -jwt검증(cookies.get_user_id 호출)
@router.get("/manage/{user_id}", response_model=PrivateUserRead)
async def get_user(user_id:int,request:Request,db:AsyncSession=Depends(get_db)) ->User:    
    await get_user_id(request)
    return await UserService.get_user(user_id,db)

#수정, 삭제는 로그인한 직원만 가능 (jwt의존성주입(get_user_id), 토큰 검증 실행만)
#회원삭제 (Delete) 
@router.delete("/delete/{user_id}")
async def delete_user(user_id:int,
                      staff_id=Depends(get_user_id),
                      db:AsyncSession=Depends(get_db)):    
    result = await UserCrud.delete_user_by_id(user_id,db)
    return {"msg":"회원삭제","deleted":result}

#회원정보수정 (Update)
@router.put("/update/{user_id}")
async def update_user_by_id(user:UserUpdate,
                            user_id:int, 
                            staff_id:int=Depends(get_user_id),
                            db:AsyncSession=Depends(get_db)):
    result = await UserCrud.update_user_by_id(user,user_id,db)    
    return result


#로그아웃
@router.get("/logout", response_model=bool)
async def logout(request:Request,response:Response):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token and not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="이미 로그아웃됨")    
    
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return True



