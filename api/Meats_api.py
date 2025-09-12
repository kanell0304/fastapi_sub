from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from domain.Meats import CreateMeat, ReadMeat
from service.Meats_service import MeatService
from database.db import get_db

router = APIRouter(prefix="/meats", tags=["Meats"])

#상품 등록
@router.post("/create", response_model= ReadMeat)
def create_meat(meat:CreateMeat,db:Session=Depends(get_db)):
    db_meat = MeatService.create_meat(meat,db)
    return db_meat