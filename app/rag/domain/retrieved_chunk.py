from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievedChunk:
    news_id: int
    chunk_index: int
    content: str
    title: str
    source: str
    url: str
