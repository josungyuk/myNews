from app.modules.news.infra.model.news_orm import NewsORM
from app.modules.news.domain.entities.news_entity import NewsEntity
from app.common.config.logging import logger

from sqlalchemy import select, exists
from sqlalchemy.orm import Session, session
from sqlalchemy.exc import IntegrityError

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

    def save_ignore_duplicate(self, news: NewsEntity) -> bool | None:
        orm = NewsORM(
            title = news.title,
            content = news.content,
            url = news.url,
            created_at = news.created_at,
            language = news.language
        )

        try:
            with self._session.begin_nested():
                self._session.add(orm)
                self._session.flush()
            return True
        except IntegrityError as e:
            # logger.error(e)
            return False

    def read_by_type(self, url: str) -> NewsEntity | None:
        stmt = select(NewsORM).where(NewsORM.url == url)
        orm = self._session.execute(stmt).scalar_one_or_none()
        
        return orm