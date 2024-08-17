# app/api/v1/router.py
from fastapi import APIRouter
from .endpoints import library, document, chunk

router = APIRouter()
router.include_router(library.router, prefix="/libraries", tags=["libraries"])
router.include_router(document.router, prefix="/documents", tags=["documents"])
router.include_router(chunk.router, prefix="/chunks", tags=["chunks"])