from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError   # id, 설명 제외한 모든 컬럼 값 동일할 경우 발생하는 에러 처리용
from domain.Meats import Meat, CreateMeat, ReadMeat, UpdateMeat, MeatInDB
from fastapi import HTTPException, status

class MeatService:

    # 생성
    @staticmethod
    async def create_meat(db:AsyncSession, create_meat:CreateMeat):
        db_meat=Meat(**create_meat.model_dump())
        db.add(db_meat)

        try:
            await db.commit()
            await db.refresh(db_meat)
            return db_meat            

        # id, 설명 제외한 모든 컬럼 값 동일할 경우
        except IntegrityError as e:   
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"동일한 상품이 존재합니다. {e}")

    # id로 조회
    @staticmethod
    async def get_meat_id(db: AsyncSession, id:int):
        db_meat = await db.get(Meat, id)  

        if not db_meat:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 id입니다")
        return db_meat  

    # 전체 데이터 조회
    @staticmethod
    async def get_all_meats(db: AsyncSession):
        result = await db.execute(select(Meat))
        db_all_meats = result.scalars().all()  

        if not db_all_meats:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="상품 데이터가 존재하지 않습니다")
        return db_all_meats

    # 데이터 수정
    @staticmethod
    async def update_meat(db:AsyncSession, id:int, update_meat:UpdateMeat):
        db_meat=await db.get(Meat, id)
        if not db_meat:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 id입니다")
       
        try:
            update_data=update_meat.model_dump(exclude_unset=True)
            for column, value in update_data.items():
                setattr(db_meat, column, value)
            await db.commit()
            await db.refresh(db_meat)
            return db_meat
       
        # 수정값과 중복되는 데이터 있을 경우
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"동일한 상품이 존재합니다. {e}")
            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")       

    # 데이터 삭제
    @staticmethod
    async def delete_meat(db: AsyncSession, id:int):
        try:
            db_meat = await db.get(Meat, id)  
            if not db_meat:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 id입니다")
            db.delete(db_meat)
            await db.commit()
            return db_meat
       
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")  