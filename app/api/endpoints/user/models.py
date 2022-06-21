from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db.models import TimeStampMixin


class User(Base, TimeStampMixin):
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    texts = relationship("Text", back_populates="owner")
