from fastapi import APIRouter

from app.api.endpoints.text.views import router as text_router

api_router = APIRouter()

api_router.include_router(text_router, prefix='/Text', tags=['Text'])
