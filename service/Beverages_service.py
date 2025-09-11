from __future__ import annotations
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_

from domain.Beverages import Beverage, BeverageCreate, BeverageUpdate

# Create
def create_beverage(db: Session, payload: BeverageCreate) -> Beverage:
    obj = Beverage(
        name=payload.name,
        type=payload.type,
        price=float(payload.price),
        volume=payload.volume,
        stock_quantity=payload.stock_quantity,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# Read (list + filters + pagination)
def list_beverages(
    db: Session,
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

    total = db.execute(stmt).scalars().all()
    total_count = len(total)

    stmt = stmt.offset(skip).limit(limit)
    rows = db.execute(stmt).scalars().all()
    return rows, total_count

# Read (detail)
def get_beverage(db: Session, beverage_id: int) -> Optional[Beverage]:
    return db.get(Beverage, beverage_id)

# Update (full/partial)
def update_beverage(db: Session, beverage_id: int, payload: BeverageUpdate) -> Optional[Beverage]:
    obj = db.get(Beverage, beverage_id)
    if not obj:
        return None

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(obj, k, float(v) if k == "price" and v is not None else v)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# Delete
def delete_beverage(db: Session, beverage_id: int) -> bool:
    obj = db.get(Beverage, beverage_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# Stock adjust (delta + / -)
def adjust_stock(db: Session, beverage_id: int, delta: int) -> Optional[Beverage]:
    obj = db.get(Beverage, beverage_id)
    if not obj:
        return None
    new_stock = max(0, (obj.stock_quantity or 0) + int(delta))
    obj.stock_quantity = new_stock
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
