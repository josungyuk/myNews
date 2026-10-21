from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.ai.embedding.embedding_client import EmbeddingClient
from app.common.config.dependencies import get_embedding_client, get_llm_client
from app.common.config.settings import settings
from app.common.db.session_setting import get_session
from app.llm.llm_client import LLMClient
from app.rag.repository.news_chunk_search_repository import NewsChunkSearchRepository
from app.rag.service.rag_service import RagService


class RagQuestion(BaseModel):
    question: str = Field(min_length=1)
    limit: int = Field(default=settings.rag_top_k, ge=1, le=5)


router = APIRouter(prefix="/rag")


@router.post("/ask")
def ask_question(
    request: RagQuestion,
    session: Session = Depends(get_session),
    embedding_client: EmbeddingClient = Depends(get_embedding_client),
    llm_client: LLMClient = Depends(get_llm_client),
):
    service = RagService(
        embedding_client=embedding_client,
        search_repository=NewsChunkSearchRepository(session),
        llm_client=llm_client,
        max_context_chars=settings.rag_max_context_chars,
    )
    return service.answer(request.question, request.limit)
