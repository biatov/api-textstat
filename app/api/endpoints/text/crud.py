from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.crud import CRUDBase
from .models import Text, Stat
from .schemas import TextCreate, TextUpdate, StatCreate, StatUpdate


class CRUDText(CRUDBase[Text, TextCreate, TextUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: TextCreate, owner_id: int
    ) -> Text:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)  # noqa
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Text]:
        return (
            db.query(self.model)
            .filter(Text.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


class CRUDTextStat(CRUDBase[Stat, StatCreate, StatUpdate]):
    def create_with_text(
        self, db: Session, *, obj_in: StatCreate, text_id: str
    ) -> Stat:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, text_id=text_id)  # noqa
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


text = CRUDText(Text)
stat = CRUDTextStat(Stat)
