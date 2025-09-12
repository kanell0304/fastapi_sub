from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from domain.Meats import CreateMeat, ReadMeat, UpdateMeat
from service.Meats_service import MeatService
from database.db import get_db

router = APIRouter(prefix="/meats", tags=["Meats"])

#상품 등록
@router.post("/create", response_model= ReadMeat)
async def create_meat(meat:CreateMeat,db:AsyncSession=Depends(get_db)):
    db_meat = await MeatService.create_meat(db,meat)
    return db_meat

@router.get("/get_id", response_model= ReadMeat)
async def get_meat_id(db:AsyncSession=Depends(get_db), id:int=Query(ge=1)):
    db_meat = await MeatService.get_meat_id(db,id)
    return db_meat

@router.get("/get_all")
async def get_all_meat(db:AsyncSession=Depends(get_db)):
    db_all_meats = await MeatService.get_all_meats(db)
    return db_all_meats

@router.post("/update", response_model= ReadMeat)
async def update_meat(meat:UpdateMeat, db:AsyncSession=Depends(get_db), id:int=Query(ge=1)):
    db_meat = await MeatService.update_meat(db,id,meat)
    return db_meat

@router.delete("/delete")
async def delete_meat(db:AsyncSession=Depends(get_db), id:int=Query(ge=1)):
    await MeatService.delete_meat(db,id)
    return {"msg":f"{id}번 삭제 완료"}