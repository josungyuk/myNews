from sqlalchemy import select

from app.ai.embedding.embedding_client import EmbeddingClient
from app.common.config.settings import settings
from app.common.db.session_setting import SessionLocal
from app.rag.domain.news_chunk_orm import NewsChunkORM


def backfill_news_embeddings(batch_size: int = 50) -> int:
    session = SessionLocal()
    embedding_client = EmbeddingClient(
        api_key=settings.llm_api_key,
        model=settings.embedding_model,
        dimension=settings.embedding_dimension,
    )

    try:
        chunks = session.execute(
            select(NewsChunkORM)
            .where(NewsChunkORM.embedding.is_(None))
            .order_by(NewsChunkORM.id)
        ).scalars().all()

        updated_count = 0
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            vectors = embedding_client.embed_documents(
                [chunk.content for chunk in batch]
            )

            for chunk, vector in zip(batch, vectors, strict=True):
                chunk.embedding = vector
                updated_count += 1

            session.commit()

        return updated_count
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    print(f"Embeddings created: {backfill_news_embeddings()}")
