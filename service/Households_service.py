from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy import select
from domain.Households import HouseHolds, HouseHoldCreate, HouseHoldUpdate, HouseHoldResponse


# @staticmethod
async def is_validate_household_by_h_id(db: AsyncSession, h_id: str):
    result = await db.execute(select(HouseHolds).filter(HouseHolds.h_id == h_id))
    if result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This household is already exists")
    return True


# @staticmethod
async def is_validate_household_by_h_name(db: AsyncSession, h_name: str):
    result = await db.execute(select(HouseHolds).filter(HouseHolds.h_name == h_name))
    if result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="household Not Found")
    return True


class Households_service:

    @staticmethod
    async def get_h_id(db: AsyncSession, h_id: int):
        result = await db.execute(select(HouseHolds).filter(HouseHolds.h_id == h_id))
        # if result is None:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="h_id Not Found")
        return result.scalar_one_or_none()


    @staticmethod
    async def get_all_household(db: AsyncSession):
        result = await db.execute(select(HouseHolds))
        # if len(result) == 0:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="household Not Found")
        return result.scalars().all()


    @staticmethod
    async def get_household_by_h_id(db: AsyncSession, h_id: int):
        result = await db.execute(select(HouseHolds).filter(HouseHolds.h_id == h_id))
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="household Not Found")
        return result.scalar_one_or_none()


    # @staticmethod
    # async def is_validate_household_by_h_id(db: AsyncSession, h_id: str):
    #     result = await db.execute(select(HouseHolds).filter(HouseHolds.h_id == h_id))
    #     if result is None:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="household Not Found")
    #     return True
    #
    # @staticmethod
    # async def is_validate_household_by_h_name(db: AsyncSession, h_name: str):
    #     result = await db.execute(select(HouseHolds).filter(HouseHolds.h_name == h_name))
    #     if result is None:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="household Not Found")
    #     return True


    @staticmethod
    async def create(db: AsyncSession, household_create: HouseHoldCreate):
        is_validate_household_by_h_name(db, household_create.h_name)
        household = household_create.model_dump()
        new_household = HouseHolds(**household)
        print(new_household)
        db.add(new_household)
        await db.commit()
        await db.refresh(new_household)

        return new_household


    @staticmethod
    async def update_household_by_h_id(db: AsyncSession, h_id: int, household_update: HouseHoldUpdate):
        household = await db.get(HouseHolds, h_id)
        if household:
            update_household = household_update.model_dump(exclude_unset=True)
            for i, j in update_household.items():
                setattr(household, i, j)
            await db.flush()
            await db.commit()
            return household
        return None


    @staticmethod
    async def delete_household_by_h_id(db: AsyncSession, h_id: int):
        household = await db.get(HouseHolds, h_id)
        if household:
            await db.delete(household)
            await db.flush()
            await db.commit()
        print(household)
        return True
