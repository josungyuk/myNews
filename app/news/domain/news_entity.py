from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=False)
class NewsEntity:
    url: str
    type: str
    source: str
    title: str
    content: str
    language: str
    created_at: datetime
    crawled_at: datetime
    world_score: int
    economy_score: int
    total_score: int
    ids: str

    @classmethod
    def from_orm(cls, orm) -> "NewsEntity":
        return cls(
            url=orm.url,
            type=orm.type,
            source=orm.source,
            title=orm.title,
            content=orm.content,
            language=orm.language,
            created_at=orm.created_at,
            crawled_at=orm.crawled_at,
            world_score=orm.world_score,
            economy_score=orm.economy_score,
            total_score=orm.total_score,
            ids=orm.ids,
        )