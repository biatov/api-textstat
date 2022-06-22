from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Path, status
from sqlalchemy.orm import Session

from app.api.endpoints.user.models import User
from app.api.endpoints.user.crud import user as crud_user
from app.api.endpoints.user.deps import get_current_active_user
from app.db.session import get_db

from .deps import check_files_path, validate_content_type
from .crud import text as crud_text
from .services import save_file
from .schemas import TextBase, TextRead, TextStats, StatArgument
from .tasks import save_stats_task, remove_text_task

router = APIRouter()

AliasPath = Path(None, alias="TextID")


@router.post(
    "/",
    response_model=TextBase,
    dependencies=[Depends(check_files_path)],
)
async def upload_text(
        db: Session = Depends(get_db),
        file: UploadFile = Depends(validate_content_type),
        current_user: User = Depends(get_current_active_user),
):
    """
    Upload file with text.
    Allowed type of files:
    * *.txt
    """
    text_db = save_file(db=db, file=file, user_id=current_user.id)
    return text_db


@router.get("/", response_model=List[TextRead])
def get_texts(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: User = Depends(get_current_active_user),
):
    """
    Get list of texts.
    """
    if crud_user.is_superuser(current_user):
        return crud_text.get_multi(db, skip=skip, limit=limit)
    return crud_text.get_multi_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.get("/{TextID}", response_model=TextStats)
def get_stats(
        text_id: str = AliasPath,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
):
    """
    Get text statistic after saving stats (__POST__: _/Text/{TextID}_ with some data).
    """
    if crud_user.is_superuser(current_user):
        text_db = crud_text.get(db=db, id=text_id)
    else:
        text_db = crud_text.get_by_owner(db=db, id=text_id, owner_id=current_user.id)
    if not text_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Text does not exist.",
        )
    return text_db


@router.post(
    "/{TextID}",
    response_model=TextBase,
    dependencies=[Depends(check_files_path)],
)
async def save_text_stats(
        *,
        text_id: str = AliasPath,
        arguments: List[StatArgument],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
):
    """
    Allowed __"name"__ field:
    * flesch_reading_ease
    * wiener_sachtextformel
        * __"argument.name"__ _"variant"_ (required)
        * __"argument.value"__ as an integer between 1 and 4
    * syllable_count
    * lexicon_count
        * __"argument.name"__ _"removepunct"_ (optional)
        * __"argument.value"__ as a bool
    * sentence_count
    * char_count
        * __"argument.name"__ _"ignore_spaces"_ (optional)
        * __"argument.value"__ as a bool
    * letter_count
        * __"argument.name"__ _"ignore_spaces"_ (optional)
        * __"argument.value"__ as a bool
    * polysyllabcount
    * monosyllabcount

    Allowed __"lang"__ field:
    * en, de, es, fr, it, nl, pl, ru
    """
    if crud_user.is_superuser(current_user):
        text_db = crud_text.get(db=db, id=text_id)
    else:
        text_db = crud_text.get_by_owner(db=db, id=text_id, owner_id=current_user.id)
    if not text_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Text does not exist.",
        )
    regular_arguments = [arg.dict() for arg in arguments]
    save_stats_task(text_id=text_id, arguments=regular_arguments)
    return text_db


@router.delete("/{TextID}", response_model=TextRead)
def delete_text(
        *,
        text_id: str = AliasPath,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user),
) -> TextRead:
    """
    Remove text with statistics.
    """
    text = crud_text.get(db=db, id=text_id)
    if not text:
        raise HTTPException(status_code=404, detail="Text not found")
    if not crud_user.is_superuser(current_user) and (text.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    remove_text_task(text_id=text_id)
    return text
