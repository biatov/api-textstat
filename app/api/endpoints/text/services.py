from typing import Union

import textstat
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings

from .crud import text, stat
from .utils import generate_internal_name, get_file_extension, read_text
from .schemas import TextCreate, TextBase, StatCreate, StatValueEnum, StatArgumentParam, LangEnum
from .tasks import upload_file_task


def save_file(db: Session, file: UploadFile) -> TextBase:
    internal_name = generate_internal_name()
    extension = get_file_extension(file.filename)
    text_in = TextCreate(
        id=internal_name,
        name=file.filename,
        content_type=file.content_type,
        extension=extension,
    )
    text_db = text.create(db=db, obj_in=text_in)

    path = f"{settings.FILE_OUT_PATH}/{internal_name}.{extension}"
    content = file.file.read().decode()
    upload_file_task(path=path, content=content)
    return text_db


def save_stats(db: Session, text_id: str, arguments: dict) -> None:
    stat_result = calculate_stat(db=db, text_id=text_id, arguments=arguments)
    if stat_result is not None:
        stat_in = StatCreate(**arguments, value=stat_result)
        stat.create_with_text(db=db, obj_in=stat_in, text_id=text_id)


def calculate_stat(db: Session, text_id: str, arguments: dict) -> Union[float, int, None]:
    lang: LangEnum = arguments.get("lang") or LangEnum.en
    callback: StatValueEnum = arguments.get("name")
    func = getattr(textstat, callback.name, None)
    if not callable(func):
        return None
    func_kwargs = {"text": read_text(db=db, text_id=text_id)}
    func_args = arguments.get("argument") or {}
    arg_name: StatArgumentParam = func_args.get("name")
    arg_value = func_args.get("value")
    if arg_name and arg_value:
        func_kwargs[arg_name.value] = arg_value
    textstat.set_lang(lang=lang.value)  # noqa
    return func(**func_kwargs)
