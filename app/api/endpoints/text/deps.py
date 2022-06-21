import os

from fastapi import UploadFile, File, HTTPException, status

from app.core.config import settings


def check_files_path() -> None:
    os.makedirs(settings.FILE_OUT_PATH, exist_ok=True)


def validate_content_type(file: UploadFile = File(alias="Text")) -> UploadFile:
    if file.content_type not in settings.FILE_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File type of '{file.content_type}' is not supported.",
        )
    return file
