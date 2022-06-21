from contextvars import ContextVar
from typing import Final, Optional
from uuid import uuid1

from fastapi import FastAPI, Request
from sqlalchemy.orm import sessionmaker, scoped_session
from starlette.middleware.cors import CORSMiddleware

from app.api.common import api_router
from app.core.config import settings
from app.db.session import engine

api = FastAPI(title=settings.PROJECT_NAME)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    api.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


@api.middleware("http")
async def db_session_middleware(request: Request, call_next):
    # https://github.com/tiangolo/fastapi/issues/726
    request_id = str(uuid1())
    ctx_token = _request_id_ctx_var.set(request_id)

    try:
        session = scoped_session(sessionmaker(bind=engine), scopefunc=get_request_id)
        request.state.db = session()
        response = await call_next(request)
    except Exception as e:
        raise e from None
    finally:
        request.state.db.close()

    _request_id_ctx_var.reset(ctx_token)
    return response


api.include_router(api_router)
