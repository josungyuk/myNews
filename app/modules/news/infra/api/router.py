from fastapi import APIRouter
from fastapi import Depends

from app.modules.news.application.usecase.crawling import Crawling
from app.modules.news.infra.crawling.client import driver_provider
from app.common.db.database import get_session
from app.modules.news.infra.repositories.news_repository import NewsRepository
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/news")
def get_news(session: Session = Depends(get_session)):
    """
    Docstring for get_news
    """

    with driver_provider() as driver:
        news_repository = NewsRepository(session)
        crawling = Crawling(news_repository)
        results = crawling.fetch_latest(driver)
      
    return results