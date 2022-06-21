from sqlalchemy import Column, String, Float, ForeignKey, Enum as SQLAlchemyEnum, Integer
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from app.api.endpoints.text.schemas import StatValueEnum, LangEnum
from app.db.models import TimeStampMixin
from app.db.base import Base


class Text(Base, TimeStampMixin):
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    content_type = Column(String, nullable=True)
    extension = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="texts")
    stats = relationship("Stat", back_populates="text")


class Stat(Base):
    name = Column(SQLAlchemyEnum(StatValueEnum))
    value = Column(Float)
    argument = Column(JSON, nullable=True)
    lang = Column(SQLAlchemyEnum(LangEnum), default=LangEnum.en)

    text_id = Column(String, ForeignKey("text.id", ondelete="CASCADE"))
    text = relationship("Text", back_populates="stats")
