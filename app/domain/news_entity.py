from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=False)
class NewsEntity:
    url: str
    type: str
    title: str
    content: str
    language: str
    created_at: datetime
    crawled_at: datetime
    world_score: int
    economy_score: int
    total_score: int
    ids: str