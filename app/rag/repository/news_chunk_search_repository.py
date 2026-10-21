from sqlalchemy import select
from sqlalchemy.orm import Session

from app.news.domain.news_orm import NewsORM
from app.rag.domain.news_chunk_orm import NewsChunkORM
from app.rag.domain.retrieved_chunk import RetrievedChunk


class NewsChunkSearchRepository:
    def __init__(self, session: Session):
        self._session = session

    def search_similar(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        stmt = (
            select(NewsChunkORM, NewsORM)
            .join(NewsORM, NewsORM.id == NewsChunkORM.news_id)
            .where(NewsChunkORM.embedding.is_not(None))
            .order_by(NewsChunkORM.embedding.cosine_distance(query_vector))
            .limit(limit)
        )

        rows = self._session.execute(stmt).all()
        return [
            RetrievedChunk(
                news_id=chunk.news_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                title=news.title,
                source=news.source,
                url=news.url,
            )
            for chunk, news in rows
        ]
