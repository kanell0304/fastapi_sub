from fastapi import APIRouter
from api.Beverages_api import router as beverages_router
from api.Households_api import router as househols_router
from api.Meats_api import router as meats_router
from api.Snacks_api import router as snacks_router
from api.Users_api import router as users_router



router = APIRouter()
router.include_router(beverages_router, prefix="/beverages", tags=["Beverages"])
router.include_router(househols_router, prefix="/households", tags=["Households"])
router.include_router(meats_router, prefix="/meats", tags=["Meats"])
router.include_router(snacks_router, prefix="/snacks", tags=["Snacks"])
router.include_router(users_router, prefix="/users", tags=["Users"])
