from fastapi import Response, Request, HTTPException,status
from security.settings import settings
from security.Jwt import validate_jwt
from jwt import InvalidTokenError

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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    try:
        user_id = validate_jwt(access_token)
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        return user_id
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="토큰만료. 갱신해주세요")

    



