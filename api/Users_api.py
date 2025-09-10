from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session

# from database.database import get_db
from domain.Users import User, UserCreate, UserUpdate, UserLogin,UserRead
from service.Users_service import UserService



router = APIRouter()

# prefix="/users"
@router.post("/signup", response_model= UserRead)
async def signup(user:UserCreate,db:AsyncSession=Depends(get_db)):
    db_user = await UserService.signup(db,user)
    return db_user
    
    