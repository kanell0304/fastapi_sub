from fastapi import APIRouter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from domain.Snacks import CreateSnack, ReadSnack
from service.Snacks_service import SnackService
from database.db import get_db

router = APIRouter(prefix="/snacks", tags=["Snacks"])

#상품 등록
@router.post("/create", response_model= ReadSnack)
def create_snack(snack:CreateSnack,db:Session=Depends(get_db)):
    db_snack = SnackService.create_snack(snack,db)
    return db_snack