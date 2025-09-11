from __future__ import annotations

from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from sqlalchemy.orm import Session

from database.db import get_db, Base, engine
from domain.Beverages import Beverage, BeverageCreate, BeverageUpdate, BeverageOut
from service.Beverages_service import (
    create_beverage,
    list_beverages,
    get_beverage,
    update_beverage,
    delete_beverage,
    adjust_stock,
)

# 테이블 자동 생성 (초기 학습/과제용)
Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/", response_model=BeverageOut, status_code=status.HTTP_201_CREATED)
def create_beverage_api(payload: BeverageCreate, db: Session = Depends(get_db)) -> BeverageOut:
    return create_beverage(db, payload)

@router.get("/", response_model=Dict[str, Any])
def list_beverages_api(
    q: Optional[str] = Query(None, description="이름/타입 검색어"),
    type: Optional[str] = Query(None, description="필터: 타입(탄산/주스/커피/차 등)"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    rows, total = list_beverages(db, q=q, type=type, min_price=min_price, max_price=max_price, skip=skip, limit=limit)
    return {
        "total": total,
        "count": len(rows),
        "items": [BeverageOut.model_validate(r) for r in rows],
    }

@router.get("/{beverage_id}", response_model=BeverageOut)
def get_beverage_api(beverage_id: int, db: Session = Depends(get_db)) -> BeverageOut:
    obj = get_beverage(db, beverage_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Beverage not found")
    return obj

@router.put("/{beverage_id}", response_model=BeverageOut)
def update_beverage_api(beverage_id: int, payload: BeverageUpdate, db: Session = Depends(get_db)) -> BeverageOut:
    obj = update_beverage(db, beverage_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Beverage not found")
    return obj

@router.delete("/{beverage_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_beverage_api(beverage_id: int, db: Session = Depends(get_db)) -> Response:
    ok = delete_beverage(db, beverage_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Beverage not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{beverage_id}/stock", response_model=BeverageOut)
def adjust_stock_api(beverage_id: int, delta: int = Query(..., description="증감 수량(+/-)"), db: Session = Depends(get_db)) -> BeverageOut:
    obj = adjust_stock(db, beverage_id, delta)
    if not obj:
        raise HTTPException(status_code=404, detail="Beverage not found")
    return obj
