from fastapi import APIRouter
from fastapi import Depends

from app.service.crawling_service import CrawlingService
from app.common.db.session_setting import get_session
from app.repository.news_repository import NewsRepository
from app.repository.news_repo_interface import NewsRepositoryInterface
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/crawls"
)

@router.get("")
def fetch_news(session: Session = Depends(get_session)):
    """
    Docstring for get_news
    """

    news_repository: NewsRepositoryInterface = NewsRepository(session)
    crwaling_service = CrawlingService(news_repository)

    results = crwaling_service.fetch_latest()
      
    return results