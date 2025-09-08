from fastapi import FastAPI
from service.api_routes import router as service_router

# FastAPI 앱 생성
app = FastAPI(
    title="My FastAPI Application",
    description="API with separated service layer",
    version="1.0.0"
)

# 서비스 라우터를 /api 프리픽스로 포함
app.include_router(
    service_router, 
    prefix="/api", 
    tags=["Service API"]
)