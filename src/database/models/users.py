from database.base import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
