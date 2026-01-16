from app.modules.news.infra.model.news_orm import NewsORM
from app.modules.news.domain.entities.news_entity import NewsEntity

from sqlalchemy import select
from sqlalchemy.orm import Session, session

class NewsRepository:
    def __init__(self, session: Session):
        self._session = session

    def save(self, news: NewsEntity) -> None:
        orm = NewsORM(
            title = news.title,
            content = news.content,
            url = news.url,
            created_at = news.created_at
        )

        self._session.add(orm)
        self._session.commit()

    def read_by_type(self, url: str) -> NewsEntity | None:
        stmt = select(NewsORM).where(NewsORM.url == url)
        orm = self._session.execute(stmt).scalar_one_or_none()
        
        if orm is None:
            return None
        
        return NewsEntity(
            title = orm.title,
            content = orm.content,
            url = orm.url,
            created_at = orm.created_at
        )