# service/Beverages_service.py
from __future__ import annotations
from typing import List, Optional, Tuple

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from domain.Beverages import Beverage, BeverageCreate, BeverageUpdate

# Create
async def create_beverage(db: AsyncSession, payload: BeverageCreate) -> Beverage:
    obj = Beverage(
        name=payload.name,
        type=payload.type,
        price=float(payload.price),
        volume=payload.volume,
        stock_quantity=payload.stock_quantity,
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

# List + filters
async def list_beverages(
    db: AsyncSession,
    q: Optional[str] = None,
    type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 20,
) -> Tuple[List[Beverage], int]:
    stmt = select(Beverage)
    conds = []

    if q:
        like = f"%{q.strip()}%"
        conds.append(or_(Beverage.name.ilike(like), Beverage.type.ilike(like)))
    if type:
        conds.append(Beverage.type == type.strip())
    if min_price is not None:
        conds.append(Beverage.price >= min_price)
    if max_price is not None:
        conds.append(Beverage.price <= max_price)

    if conds:
        stmt = stmt.where(and_(*conds))

    # total
    res_all = await db.execute(stmt)
    total_count = len(res_all.scalars().all())

    # page
    res = await db.execute(stmt.offset(skip).limit(limit))
    rows = res.scalars().all()
    return rows, total_count

# Detail
async def get_beverage(db: AsyncSession, beverage_id: int) -> Optional[Beverage]:
    return await db.get(Beverage, beverage_id)

# Update
async def update_beverage(db: AsyncSession, beverage_id: int, payload: BeverageUpdate) -> Optional[Beverage]:
    obj = await db.get(Beverage, beverage_id)
    if not obj:
        return None
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, float(v) if k == "price" and v is not None else v)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

# Delete
async def delete_beverage(db: AsyncSession, beverage_id: int) -> bool:
    obj = await db.get(Beverage, beverage_id)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True

# Stock adjust
async def adjust_stock(db: AsyncSession, beverage_id: int, delta: int) -> Optional[Beverage]:
    obj = await db.get(Beverage, beverage_id)
    if not obj:
        return None
    obj.stock_quantity = max(0, (obj.stock_quantity or 0) + int(delta))
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj
