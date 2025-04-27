from sqlalchemy.orm import (
    Mapped,
    relationship
)
from typing import List

from .base import Base, uniq_str


class User(Base):
    name: Mapped[uniq_str]
    email: Mapped[uniq_str]
    password: Mapped[bytes]
    photo_filename: Mapped[str]
    active: Mapped[bool]

    tokens: Mapped[List["Token"]] = relationship(
        "Token",
        back_populates="user",
        cascade="all, delete-orphan"
    )
