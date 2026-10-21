from fastapi import APIRouter
from fastapi import Depends

from app.news.service.news_service import CrawlingService
from app.common.db.session_setting import get_session
from app.news.repository.news_repository import NewsRepository
from app.news.repository.news_repo_interface import NewsRepositoryInterface
from app.rag.service.chunking_service import ChunkingService
from app.rag.repository.news_chunk_repository import NewsChunkRepository
from app.common.config.dependencies import get_chunk_embedding_service
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/news"
)

@router.post("")
def fetch_news(session: Session = Depends(get_session)):
    """
    Docstring for get_news
    """

    news_repository: NewsRepositoryInterface = NewsRepository(session)
    news_chunk_repository = NewsChunkRepository(session)
    chunking_service = ChunkingService()
    chunk_embedding_service = get_chunk_embedding_service()
    crawling_service = CrawlingService(
        news_repository,
        chunking_service,
        news_chunk_repository,
        chunk_embedding_service,
    )

    results = crawling_service.fetch_latest()
      
    return results
