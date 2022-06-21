import os
import uuid

from sqlalchemy.orm import Session

from app.core.config import settings
from .crud import text
from .deps import check_file_path
from .models import Text


def generate_internal_name() -> str:
    return str(uuid.uuid4())


def get_file_extension(file_name: str) -> str:
    return file_name.rsplit(".", 1)[-1]


def read_text(db: Session, text_id: str) -> str:
    path = get_text_path(db=db, text_id=text_id)
    return read_file(path)


def read_file(path: str) -> str:
    try:
        with open(path) as file:
            return file.read()
    except (FileNotFoundError, OSError):
        return ""


def upload_file(path: str, content: str) -> None:
    check_file_path(path)
    try:
        with open(path, "w") as file:
            file.write(content)
    except (FileNotFoundError, OSError):
        return None


def remove_file(path: str) -> None:
    try:
        os.remove(path)
    except (FileNotFoundError, OSError):
        return None


def get_text_path(db: Session, text_id: str) -> str:
    text_db: Text = text.get(db=db, id=text_id)
    if not text_db:
        return ""
    return f"{settings.FILE_OUT_PATH}/{text_db.owner_id}/{text_db.id}.{text_db.extension}"
