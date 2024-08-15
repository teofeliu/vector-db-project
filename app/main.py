# app/main.py
from fastapi import FastAPI
from app.api.v1.router import router
from app.core.config import settings

app = FastAPI(title="Vector DB API")

app.include_router(router, prefix=settings.API_V1_STR)