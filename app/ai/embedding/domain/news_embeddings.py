from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class NewsEmbedding:
    id: int
    news_id: int
    embedding: str
    embedding_model: str
    embedding_demension: int
    content_hash: str
    created_at: datetime