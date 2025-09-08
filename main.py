from fastapi import FastAPI
from service.api_routes import router

app = FastAPI(
    title="My FastAPI Service",
    description="API with separated service layer",
    version="1.0.0"
)

# service 라우터를 /api 프리픽스로 포함
app.include_router(router, prefix="/api", tags=["API Services"])

@app.get("/")
def main_root():
    return {"message": "Main application running"}