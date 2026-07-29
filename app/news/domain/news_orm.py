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

    source: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    type: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    language: Mapped[str] = mapped_column(
        String(3),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    crawled_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    world_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    economy_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    total_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    ids: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )