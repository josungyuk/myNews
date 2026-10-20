"""create news chunks

Revision ID: 71dc76aacd6e
Revises: bc8b9739a510
Create Date: 2026-10-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "71dc76aacd6e"
down_revision: Union[str, Sequence[str], None] = "bc8b9739a510"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "news_chunks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("news_id", sa.Integer(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["news_id"],
            ["news.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "news_id",
            "chunk_index",
            name="uq_news_chunks_news_id_chunk_index",
        ),
    )
    op.create_index(
        "ix_news_chunks_news_id",
        "news_chunks",
        ["news_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_news_chunks_news_id", table_name="news_chunks")
    op.drop_table("news_chunks")
