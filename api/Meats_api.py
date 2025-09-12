from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from domain.Meats import CreateMeat, ReadMeat
from service.Meats_service import MeatService
from database.db import get_db

router = APIRouter(prefix="/meats", tags=["Meats"])

#상품 등록
@router.post("/create", response_model= ReadMeat)
async def create_meat(meat:CreateMeat, db:AsyncSession=Depends(get_db)):
    db_meat = await MeatService.create_meat(db, meat)
    return db_meat