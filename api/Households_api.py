from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from domain.Households import HouseHoldCreate, HouseHoldUpdate, HouseHoldResponse
from service.Households_service import HouseholdsService

router = APIRouter(prefix="/households", tags=["HouseHolds"])

@router.post("/create", response_model=HouseHoldResponse)
async def create_household(household: HouseHoldCreate, db: AsyncSession=Depends(get_db)):
    result = await HouseholdsService.create(db, household)
    return result

@router.get("/get_households", response_model=List[HouseHoldResponse])
async def get_all_households(db: AsyncSession=Depends(get_db)):
    result = await HouseholdsService.get_all_household(db)
    return result

@router.get("/get_household/{h_id}", response_model=HouseHoldResponse)
async def get_household_by_h_id(h_id: int, db: AsyncSession=Depends(get_db)):
    result = await HouseholdsService.get_household_by_h_id(db, h_id)
    return result

@router.put("/update/{h_id}", response_model=HouseHoldResponse)
async def update_household_by_h_id(h_id: int, household: HouseHoldUpdate, db: AsyncSession=Depends(get_db)):
    result = await HouseholdsService.update_household_by_h_id(db, h_id, household)
    return result

@router.delete("/delete/{h_id}")
async def delete_household_by_h_id(h_id: int, db: AsyncSession=Depends(get_db)):
    result = await HouseholdsService.delete_household_by_h_id(db, h_id)
    if result:
        return {"msg": "Delete Success"}
    else:
        return {"msg": "Delete Failed"}
