from typing import Optional, Union

import aiofiles
import textstat
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings

from .crud import text, stat
from .utils import get_file_extension, read_text
from .schemas import TextCreate, TextBase, StatCreate, StatValueEnum, StatArgumentParam, LangEnum


async def upload_file(
        file: UploadFile,
        internal_name: str,
        path: Optional[str] = settings.FILE_OUT_PATH,
        chunk_size: Optional[int] = settings.FILE_CHUNK_SIZE,
) -> None:
    extension = get_file_extension(file.filename)
    async with aiofiles.open(f"{path}/{internal_name}.{extension}", "wb") as out_file:
        while content := await file.read(chunk_size):
            await out_file.write(content)


def create(db: Session, file: UploadFile, internal_name: str) -> TextBase:
    text_in = TextCreate(
        name=file.filename,
        id=internal_name,
        content_type=file.content_type,
        extension=get_file_extension(file.filename),
    )
    text.create(db=db, obj_in=text_in)
    return TextBase(id=text_in.id)


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
