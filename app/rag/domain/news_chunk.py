from dataclasses import dataclass

@dataclass(frozen=True)
class NewsChunk:
    news_id: int
    chunk_index: int
    content: str
    content_hash: str