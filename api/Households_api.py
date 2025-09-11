from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from domain.Households import HouseHoldCreate, HouseHoldUpdate
from service.Households_service import Households_service

router = APIRouter(prefix="/households", tags=["HouseHolds"])

# 임시 선언
def get_db():
    pass

@router.post("/create")
async def create_household(household: HouseHoldCreate, db: AsyncSession=Depends(get_db)):
    result = await Households_service.create(db, household)
    return result

@router.get("/get_households")
async def get_all_households(db: AsyncSession=Depends(get_db)):
    result = await Households_service.get_all_household(db)
    return result

@router.get("/get_household/{h_id}")
async def get_household_by_h_id(h_id: int, db: AsyncSession=Depends(get_db)):
    result = await Households_service.get_household_by_h_id(db, h_id)
    return result

@router.put("/update/{h_id}")
async def update_household_by_h_id(h_id: int, household: HouseHoldUpdate, db: AsyncSession=Depends(get_db)):
    result = await Households_service.update_household_by_h_id(db, h_id, household)
    return result

@router.delete("/delete/{h_id}")
async def delete_household_by_h_id(h_id: int, db: AsyncSession=Depends(get_db)):
    result = await Households_service.delete_household_by_h_id(db, h_id)
    return {"msg": "Delete Success", "deleted household": result}
