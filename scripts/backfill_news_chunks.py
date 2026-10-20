from sqlalchemy import exists, select

from app.common.db.session_setting import SessionLocal
from app.news.domain.news_orm import NewsORM
from app.rag.domain.news_chunk_orm import NewsChunkORM
from app.rag.repository.news_chunk_repository import NewsChunkRepository
from app.rag.service.chunking_service import ChunkingService


def backfill_news_chunks() -> tuple[int, int]:
    session = SessionLocal()

    try:
        stmt = (
            select(NewsORM.id, NewsORM.content)
            .where(
                ~exists(
                    select(NewsChunkORM.id).where(
                        NewsChunkORM.news_id == NewsORM.id
                    )
                )
            )
            .order_by(NewsORM.id)
        )

        articles = session.execute(stmt).all()
        chunking_service = ChunkingService()
        chunk_repository = NewsChunkRepository(session)
        chunk_count = 0

        for news_id, content in articles:
            chunks = chunking_service.chunk(
                news_id=news_id,
                content=content,
            )
            chunk_repository.save_all(chunks)
            chunk_count += len(chunks)

        session.commit()
        return len(articles), chunk_count

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    article_count, chunk_count = backfill_news_chunks()
    print(
        f"Backfill complete: {article_count} articles, "
        f"{chunk_count} chunks created"
    )
