from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.db import get_db
from domain.Users import User, UserCreate, UserUpdate,StaffLogin,UserRead
from service.Users_service import UserService

router = APIRouter()

prefix="/users"
@router.post("/signup", response_model= UserRead)
def signup(user:UserCreate,db:Session=Depends(get_db)):
    db_user = UserService.signup(user,db)
    return db_user
    
    