from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from app.common.db.base import Base

class SummaryORM(Base):
    __tablename__ = "summary"

    id:Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    importance_score: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    key_points: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False
    )

    keywords: Mapped[list[str]] = mapped_column(
        JSONB,
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(15),
        nullable=False
    )

    model_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    prompt_version: Mapped[str] = mapped_column(
        String(15),
        nullable=False
    )

    input_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    output_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    total_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )