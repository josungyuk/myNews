from fastapi import APIRouter
from fastapi import Depends

from app.service.crawling_service import CrawlingService
from app.common.db.session_setting import get_session
from app.repository.news_repository import NewsRepository
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/news")
def get_news(session: Session = Depends(get_session)):
    """
    Docstring for get_news
    """

    news_repository = NewsRepository(session)
    crwaling_service = CrawlingService(news_repository)

    results = crwaling_service.fetch_latest()
      
    return results