from fastapi import APIRouter

from app.api.endpoints.auth.views import router as auth_router
from app.api.endpoints.user.views import router as user_router
from app.api.endpoints.text.views import router as text_router

api_router = APIRouter()

api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(text_router, prefix='/Text', tags=['Text'])
