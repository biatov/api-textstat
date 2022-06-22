from typing import Optional

from sqlalchemy.orm import Session

from app.api.endpoints.text.models import Text
from app.api.endpoints.text import crud
from app.api.endpoints.text.schemas import TextCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_text_id, random_content_type, random_extension


def create_random_text(db: Session, *, owner_id: Optional[int] = None) -> Text:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    text_id = random_text_id()
    name = random_lower_string()
    content_type = random_content_type()
    extension = random_extension()
    text_in = TextCreate(id=text_id, name=name, content_type=content_type, extension=extension)
    return crud.text.create_with_owner(db=db, obj_in=text_in, owner_id=owner_id)


def get_text_db(db: Session, *, text_id: str) -> Text:
    return crud.text.get(db=db, id=text_id)
