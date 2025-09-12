from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError   # id, 설명 제외한 모든 컬럼 값 동일할 경우 발생하는 에러 처리용
from domain.Snacks import Snack, CreateSnack, ReadSnack, UpdateSnack, SnackInDB
from fastapi import HTTPException, status

class SnackService:

    # 생성
    @staticmethod
    async def create_snack(db:AsyncSession, create_snack:CreateSnack):
        db_snack=Snack(**create_snack.model_dump())
        db.add(db_snack)

        try:
            await db.commit()
            await db.refresh(db_snack)
            return db_snack            

        except Exception as e:   
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)

    # id로 조회
    @staticmethod
    async def get_snack_id(db: AsyncSession, id:int):
        db_snack = await db.get(Snack, id)  

        if not db_snack:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 id입니다")
        return db_snack  

    # 전체 데이터 조회
    @staticmethod
    async def get_all_snacks(db: AsyncSession):
        result = await db.execute(select(Snack))
        db_all_snacks = result.scalars().all()  

        if not db_all_snacks:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="상품 데이터가 존재하지 않습니다")
        return db_all_snacks

    # 데이터 수정
    @staticmethod
    async def update_snack(db:AsyncSession, id:int, update_snack:UpdateSnack):
        db_snack=await db.get(Snack, id)
        if not db_snack:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 id입니다")
       
        try:
            update_data=update_snack.model_dump(exclude_unset=True)
            for column, value in update_data.items():
                setattr(db_snack, column, value)
            await db.commit()
            await db.refresh(db_snack)
            return db_snack
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)       

    # 데이터 삭제
    @staticmethod
    async def delete_snack(db: AsyncSession, id:int):
        db_snack = await db.get(Snack, id)  
        if not db_snack:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="존재하지 않는 id입니다")
       
        try:
            db.delete(db_snack)
            await db.commit()
            return db_snack
       
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")  