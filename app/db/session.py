from fastapi import Request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_size=settings.DATABASE_ENGINE_POOL_SIZE,
    max_overflow=settings.DATABASE_ENGINE_MAX_OVERFLOW,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db(request: Request):
    session: Session = request.state.db
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
