from fastapi import Response
from security import settings
from security.Jwt import validate_jwt

def set_cookies(response:Response, access_token:str, refresh_token):
    pass

