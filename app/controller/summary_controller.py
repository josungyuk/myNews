from fastapi import APIRouter
from fastapi import Depends

from app.common.db.session_setting import get_session
from sqlalchemy.orm import Session
from app.common.config.dependencies import get_llm_client
from app.llm.llm_client import LLMClient
from app.repository.news_repo_interface import NewsRepositoryInterface
from app.repository.news_repository import NewsRepository
from app.repository.summary_repo_interface import SummaryRepositoryInterface
from app.repository.summary_repository import SummaryRepository
from app.service.summary_service import SummaryService

router = APIRouter(
    prefix="/summaries",
)

@router.get("/economy")
def get_economy_summary(session: Session = Depends(get_session), llm_client: LLMClient = Depends(get_llm_client)):
    news_repository: NewsRepositoryInterface = NewsRepository(session)
    summary_repository: SummaryRepositoryInterface = SummaryRepository(session)
    

    summary_service = SummaryService(
        llm_client, 
        news_repository, 
        summary_repository
    )

    result = summary_service.summary_economy_priority()
    # result = summary_service.test()

    return result