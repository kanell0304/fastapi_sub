from fastapi import APIRouter, Depends
from fastapi import HTTPException, status


from sqlalchemy import select
from sqlalchemy.orm import Session

from database.db import get_db
from domain.Users import User, UserCreate, UserUpdate,StaffLogin,UserRead
from service.Users_service import UserService

#dummy DB
# async_engine = "dummyDB"
# AsyncSessionLocal = sessionmaker(
#     autocommit=False, autoflush=False, bind=async_engine, class_=Session
# )
# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session
#--- end ---

router = APIRouter()

prefix="/users"
@router.post("/signup", response_model= UserRead)
async def signup(user:UserCreate,db:Session=Depends(get_db)):
    db_user = await UserService.signup(db,user)
    return db_user
    
    