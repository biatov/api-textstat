from typing import Union, List

import textstat
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from .crud import text as crud_text, stat
from .utils import generate_internal_name, get_file_extension, read_text, get_text_path, remove_file, generate_file_path
from .schemas import TextCreate, TextBase, StatCreate, StatUpdate, StatValueEnum, ArgumentParamEnum, LangEnum


def save_file(db: Session, file: UploadFile, user_id: int) -> TextBase:
    internal_name = generate_internal_name()
    extension = get_file_extension(file.filename)
    text_in = TextCreate(
        id=internal_name,
        name=file.filename,
        content_type=file.content_type,
        extension=extension,
    )
    text_db = crud_text.create_with_owner(db=db, obj_in=text_in, owner_id=user_id)

    path = generate_file_path(user_id=user_id, text_id=internal_name, extension=extension)
    content = file.file.read().decode()
    from .tasks import upload_file_task  # noqa
    upload_file_task(path=path, content=content)
    return text_db


def remove_text(text_id: str) -> TextBase:
    db = SessionLocal()
    path = get_text_path(db=db, text_id=text_id)
    text = crud_text.remove(db=db, id=text_id)
    remove_file(path=path)
    return text


def save_stats(text_id: str, arguments: List[dict]) -> None:
    db = SessionLocal()
    text = read_text(db=db, text_id=text_id)
    for argument in arguments:
        exists = stat.get_full_match(db=db, obj_in=StatUpdate(**argument), text_id=text_id)
        if exists:
            continue
        stat_result = calculate_stat(text=text, arguments=argument)
        if stat_result is None:
            continue
        stat_in = StatCreate(**argument, value=stat_result)
        stat.create_with_text(db=db, obj_in=stat_in, text_id=text_id)


def calculate_stat(text: str, arguments: dict) -> Union[float, int, None]:
    lang: LangEnum = arguments.get("lang") or LangEnum.en
    callback = StatValueEnum(arguments.get("name"))
    func = getattr(textstat, callback.value, None)
    if not callable(func):
        return None
    func_kwargs = {"text": text}
    func_args = arguments.get("argument") or {}
    arg_name = func_args.get("name")
    arg_value = func_args.get("value")
    if arg_name and arg_value is not None:
        func_kwargs[ArgumentParamEnum(arg_name).value] = arg_value
    textstat.set_lang(lang=lang)  # noqa
    return func(**func_kwargs)
