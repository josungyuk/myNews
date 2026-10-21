"""add embeddings to news chunks

Revision ID: c1f5e6a7b8c9
Revises: 71dc76aacd6e
Create Date: 2026-10-21

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision: str = "c1f5e6a7b8c9"
down_revision: Union[str, Sequence[str], None] = "71dc76aacd6e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column(
        "news_chunks",
        sa.Column("embedding", Vector(768), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("news_chunks", "embedding")
