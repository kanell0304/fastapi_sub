from fastapi import Response, Request, HTTPException,status
from fastapi.responses import JSONResponse
from security.settings import settings
from security.Jwt import validate_jwt,create_access_token, create_refresh_token
from service.Users_service import UserCrud
from jwt import InvalidTokenError,ExpiredSignatureError

def set_cookies(response:Response, access_token:str, refresh_token:str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=int(settings.access_token_lifetime.total_seconds())
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=int(settings.refresh_token_lifetime.total_seconds())
    )

#토큰 검증시 의존성주입, access_token 검증, user_id 반환
async def get_user_id(request:Request):
    access_token = request.cookies.get("access_token")    

    #에외처리
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="로그인한 직원만 사용가능")
    
    try:
        user_id = validate_jwt(access_token)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        return user_id
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="토큰만료. 갱신해주세요")

#토큰 갱신 후 쿠키 갱신 
async def refresh_expired_token(request:Request, response:Response,db):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        try:
            user_id = validate_jwt(refresh_token)
        except (ExpiredSignatureError,InvalidTokenError):
            return response
        
        new_access_token = create_access_token(user_id)
        new_refresh_token = create_refresh_token(user_id) 

        await UserCrud.update_refresh_token(user_id,new_refresh_token,db)
        await db.commit()

        set_cookies(response,new_access_token,new_refresh_token)
    return JSONResponse(content={"access_token":new_access_token})


