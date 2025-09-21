from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from app.database.session import engine
from app.database.session import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="User Task Manager.",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)