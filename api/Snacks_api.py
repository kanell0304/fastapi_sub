from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from domain.Snacks import CreateSnack, ReadSnack, UpdateSnack
from service.Snacks_service import SnackService
from database.db import get_db

router = APIRouter(prefix="/snacks", tags=["Snacks"])

#상품 등록
@router.post("/create", response_model= ReadSnack)
async def create_snack(snack:CreateSnack,db:AsyncSession=Depends(get_db)):
    db_snack = await SnackService.create_snack(db,snack)
    return db_snack

@router.get("/get_id", response_model= ReadSnack)
async def get_snack_id(db:AsyncSession=Depends(get_db), id:int=Query(ge=1)):
    db_snack = await SnackService.get_snack_id(db,id)
    return db_snack

@router.get("/get_all")
async def get_snack_id(db:AsyncSession=Depends(get_db)):
    db_all_snacks = await SnackService.get_all_snacks(db)
    return db_all_snacks

@router.post("/update", response_model= ReadSnack)
async def get_snack_id(snack:UpdateSnack, db:AsyncSession=Depends(get_db), id:int=Query(ge=1)):
    db_snack = await SnackService.update_snack(db,id,snack)
    return db_snack

@router.delete("/delete")
async def delete_meat(db:AsyncSession=Depends(get_db), id:int=Query(ge=1)):
    await SnackService.delete_meat(db,id)
    return {"msg":f"{id}번 삭제 완료"}