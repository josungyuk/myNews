from app.common.config.settings import settings
from app.ai.embedding.embedding_client import EmbeddingClient
from app.llm.llm_client import LLMClient


def get_llm_client() -> LLMClient:
    return LLMClient(
        api_key=settings.llm_api_key,
        model=settings.llm_model
    )


def get_embedding_client() -> EmbeddingClient:
    return EmbeddingClient(
        api_key=settings.llm_api_key,
        model=settings.embedding_model,
        dimension=settings.embedding_dimension,
    )
