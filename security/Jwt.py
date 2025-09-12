from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from security.settings import settings
import jwt


pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(uid:int) -> str:
    return create_jwt(uid=uid, expire=settings.access_token_lifetime)

def create_refresh_token(uid:int) ->str:
    return create_jwt(uid=uid, expire=settings.refresh_token_lifetime)

def create_jwt(uid:int, expire:timedelta, **kwargs) -> str:
    to_encode = kwargs.copy()
    exp = datetime.now(timezone.utc) + expire
    to_encode.update({"sub":uid,"exp":exp})
    encoded_token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_token

def validate_jwt(token:str)->int:
    payload=jwt.decode(token, settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    return payload.get("sub")

