from app.news.domain.news_orm import NewsORM
from app.news.domain.news_entity import NewsEntity
from app.common.config.logging import logger

from sqlalchemy import select, exists
from sqlalchemy.orm import Session, session
from sqlalchemy.exc import IntegrityError

from datetime import datetime, date, time

class NewsRepository:
    def __init__(self, session: Session):
        self._session = session

    def save(self, news: NewsEntity) -> bool:
        orm = NewsORM(
            title = news.title,
            type = news.type,
            content = news.content,
            url = news.url,
            language = news.language,
            created_at = news.created_at,
            crawled_at = news.crawled_at,
            world_score = news.world_score,
            economy_score = news.economy_score,
            total_score = news.total_score,
            ids = news.ids
        )

        self._session.add(orm)
        self._session.commit()

    def save_ignore_duplicate(self, news: NewsEntity) -> bool:
        orm = NewsORM(
            title = news.title,
            type = news.type,
            content = news.content,
            url = news.url,
            language = news.language,
            created_at = news.created_at,
            crawled_at = news.crawled_at,
            world_score = news.world_score,
            economy_score = news.economy_score,
            total_score = news.total_score,
            ids = news.ids
        )

        try:
            with self._session.begin_nested():
                self._session.add(orm)
                self._session.flush()
            return True
        except IntegrityError as e:
            logger.error("Fail to save news due to integrity error: ", e)
            return False
        
    def read_economy_score_priority(self, ) -> list[NewsEntity]:
        today_start = datetime.combine(date.today(), time.min)

        # NewsORM.crawled_at >= today_start
        stmt = select(NewsORM).where().order_by(NewsORM.economy_score.desc()).limit(20)
        orm_list = self._session.execute(stmt).scalars().all()

        return [
            NewsEntity.from_orm(orm)
            for orm in orm_list
        ]
    
    def read_world_score_priority(self, ) -> list[NewsEntity]:
        today_start = datetime.combine(date.today(), time.min)

        stmt = select(NewsORM).where(NewsORM.created_at >= today_start).order_by(NewsORM.world_score.desc()).limit(20)
        orm_list = self._session.execute(stmt).scalars().all()

        return [
            NewsEntity.from_orm(orm)
            for orm in orm_list
        ]
    
    def read_total_score_priority(self, ) -> list[NewsEntity]:
        today_start = datetime.combine(date.today(), time.min)

        stmt = select(NewsORM).where(NewsORM.created_at >= today_start).order_by(NewsORM.total_score.desc()).limit(20)
        orm_list = self._session.execute(stmt).scalars().all()

        return [
            NewsEntity.from_orm(orm)
            for orm in orm_list
        ]