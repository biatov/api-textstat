from sqlalchemy.orm import Session

from app.api.endpoints.text import crud
from app.api.endpoints.text.schemas import TextCreate, TextUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string, random_text_id, random_content_type, random_extension


def test_create_item(db: Session) -> None:
    text_id = random_text_id()
    name = random_lower_string()
    content_type = random_content_type()
    extension = random_extension()
    text_in = TextCreate(id=text_id, name=name, content_type=content_type, extension=extension)
    user = create_random_user(db)
    text = crud.text.create_with_owner(db=db, obj_in=text_in, owner_id=user.id)
    assert text.id == text_id
    assert text.name == name
    assert text.content_type == content_type
    assert text.extension == extension
    assert text.owner_id == user.id


def test_get_text(db: Session) -> None:
    text_id = random_text_id()
    name = random_lower_string()
    content_type = random_content_type()
    extension = random_extension()
    text_in = TextCreate(id=text_id, name=name, content_type=content_type, extension=extension)
    user = create_random_user(db)
    text = crud.text.create_with_owner(db=db, obj_in=text_in, owner_id=user.id)
    stored_text = crud.text.get(db=db, id=text.id)
    assert stored_text
    assert text.id == stored_text.id
    assert text.name == stored_text.name
    assert text.content_type == stored_text.content_type
    assert text.extension == stored_text.extension
    assert text.owner_id == stored_text.owner_id


def test_update_text(db: Session) -> None:
    text_id = random_text_id()
    name = random_lower_string()
    content_type = random_content_type()
    extension = random_extension()
    text_in = TextCreate(id=text_id, name=name, content_type=content_type, extension=extension)
    user = create_random_user(db)
    text = crud.text.create_with_owner(db=db, obj_in=text_in, owner_id=user.id)
    name2 = random_lower_string()
    text_update = TextUpdate(name=name2)
    text2 = crud.text.update(db=db, db_obj=text, obj_in=text_update)
    assert text.id == text2.id
    assert text.content_type == text2.content_type
    assert text.extension == text2.extension
    assert text.name == text2.name
    assert text2.name == name2
    assert text.owner_id == text2.owner_id


def test_delete_text(db: Session) -> None:
    text_id = random_text_id()
    name = random_lower_string()
    content_type = random_content_type()
    extension = random_extension()
    text_in = TextCreate(id=text_id, name=name, content_type=content_type, extension=extension)
    user = create_random_user(db)
    text = crud.text.create_with_owner(db=db, obj_in=text_in, owner_id=user.id)
    text2 = crud.text.remove(db=db, id=text.id)
    text3 = crud.text.get(db=db, id=text.id)
    assert text3 is None
    assert text2.id == text.id
    assert text2.name == name
    assert text2.content_type == content_type
    assert text2.extension == extension
    assert text2.owner_id == user.id
