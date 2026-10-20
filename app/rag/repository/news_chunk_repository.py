from sqlalchemy.orm import Session

from app.rag.domain.news_chunk import NewsChunk
from app.rag.domain.news_chunk_orm import NewsChunkORM


class NewsChunkRepository:
    def __init__(self, session: Session):
        self._session = session

    def save_all(self, chunks: list[NewsChunk]) -> None:
        if not chunks:
            return

        orm_chunks = [
            NewsChunkORM(
                news_id=chunk.news_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                content_hash=chunk.content_hash,
            )
            for chunk in chunks
        ]

        self._session.add_all(orm_chunks)
        self._session.flush()
