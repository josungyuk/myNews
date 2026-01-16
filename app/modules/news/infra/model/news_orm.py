from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.common.db.base import Base

class NewsORM(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    hash_id: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )