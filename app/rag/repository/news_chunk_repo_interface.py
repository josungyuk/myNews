from typing import Protocol

from app.rag.domain.news_chunk import NewsChunk


class NewsChunkRepositoryInterface(Protocol):
    def save_all(self, chunks: list[NewsChunk]) -> None: ...
