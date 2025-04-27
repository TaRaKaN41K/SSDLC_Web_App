from sqlalchemy import (
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .base import Base, uniq_str


class Token(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    token: Mapped[uniq_str]
    device_id: Mapped[str] = mapped_column()
    UniqueConstraint(user_id, device_id, name="uix_user_device")

    user: Mapped["User"] = relationship(
        "User",
        back_populates="tokens"
    )
