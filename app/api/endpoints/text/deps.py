import errno
import os

from fastapi import UploadFile, File, HTTPException, status

from app.core.config import settings


def check_files_path() -> None:
    check_file_path(path=settings.FILE_OUT_PATH)


def check_file_path(path: str) -> None:
    if os.path.exists(path):
        return None
    try:
        os.makedirs(os.path.dirname(path))
    except FileNotFoundError:
        return None
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise exc


def validate_content_type(file: UploadFile = File(alias="Text")) -> UploadFile:
    if file.content_type not in settings.FILE_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File type of '{file.content_type}' is not supported.",
        )
    return file
