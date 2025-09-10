from fastapi import APIRouter

router = APIRouter()

# prefix="/users"
@router.post("/")
async def create_user():
    pass