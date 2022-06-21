from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Path, status
from sqlalchemy.orm import Session

from app.db.session import get_db

from .deps import check_files_path, validate_content_type
from .crud import text as crud_text
from .services import save_stats, save_file
from .schemas import TextBase, TextRead, TextStats, StatArgument

router = APIRouter()


@router.post(
    "/",
    response_model=TextBase,
    dependencies=[Depends(check_files_path)],
)
async def upload_text(
        db: Session = Depends(get_db),
        file: UploadFile = Depends(validate_content_type),
):
    text_db = save_file(db=db, file=file)
    return text_db


@router.get("/", response_model=List[TextRead])
def get_texts(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
):
    return crud_text.get_multi(db, skip=skip, limit=limit)


@router.get("/{TextID}", response_model=TextStats)
def get_stats(
        text_id: str = Path(None, alias="TextID"),
        db: Session = Depends(get_db),
):
    text_db = crud_text.get(db=db, id=text_id)
    if not text_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Text does not exist.",
        )
    return text_db


@router.post(
    "/{TextID}",
    response_model=TextStats,
    dependencies=[Depends(check_files_path)],
)
async def save_text_stats(
        *,
        text_id: str = Path(None, alias="TextID"),
        arguments: List[StatArgument],
        db: Session = Depends(get_db),
):
    text_db = crud_text.get(db=db, id=text_id)
    if not text_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Text does not exist.",
        )
    for argument in arguments:
        save_stats(db=db, text_id=text_id, arguments=argument.dict())
    return text_db
