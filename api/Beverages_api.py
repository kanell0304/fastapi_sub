# api/Beverages_api.py
from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from domain.Beverages import BeverageOut, BeverageCreate, BeverageUpdate
from service.Beverages_service import (
    create_beverage, list_beverages, get_beverage,
    update_beverage, delete_beverage, adjust_stock,
)

router = APIRouter()  # ✅ 이 줄이 반드시 데코레이터들보다 위!

@router.post("/", response_model=BeverageOut, status_code=status.HTTP_201_CREATED)
async def create_beverage_api(payload: BeverageCreate, db: AsyncSession = Depends(get_db)) -> BeverageOut:
    return await create_beverage(db, payload)

@router.get("/", response_model=dict)
async def list_beverages_api(
    q: str | None = Query(None),
    type: str | None = Query(None),
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    rows, total = await list_beverages(db, q=q, type=type, min_price=min_price, max_price=max_price, skip=skip, limit=limit)
    return {"total": total, "count": len(rows), "items": [BeverageOut.model_validate(r) for r in rows]}

@router.get("/{beverage_id}", response_model=BeverageOut)
async def get_beverage_api(beverage_id: int, db: AsyncSession = Depends(get_db)) -> BeverageOut:
    obj = await get_beverage(db, beverage_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Beverage not found")
    return obj

@router.put("/{beverage_id}", response_model=BeverageOut)
async def update_beverage_api(beverage_id: int, payload: BeverageUpdate, db: AsyncSession = Depends(get_db)) -> BeverageOut:
    obj = await update_beverage(db, beverage_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Beverage not found")
    return obj

@router.delete("/{beverage_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_beverage_api(beverage_id: int, db: AsyncSession = Depends(get_db)) -> Response:
    ok = await delete_beverage(db, beverage_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Beverage not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{beverage_id}/stock", response_model=BeverageOut)
async def adjust_stock_api(beverage_id: int, delta: int = Query(...), db: AsyncSession = Depends(get_db)) -> BeverageOut:
    obj = await adjust_stock(db, beverage_id, delta)
    if not obj:
        raise HTTPException(status_code=404, detail="Beverage not found")
    return obj
