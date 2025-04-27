from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import Integer
from typing import Annotated

uniq_str = Annotated[str, mapped_column(unique=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'
