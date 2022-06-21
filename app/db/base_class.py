import re

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = re.split("(?=[A-Z])", name)  # noqa
    return "_".join([x.lower() for x in names if x])


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True)

    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return resolve_table_name(self.__name__)
