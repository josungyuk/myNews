from app.common.config.settings import settings
from app.ai.embedding.embedding_client import EmbeddingClient
from app.llm.llm_client import LLMClient
from app.rag.service.chunk_embedding_service import ChunkEmbeddingService


def get_llm_client() -> LLMClient:
    return LLMClient(
        api_key=settings.llm_api_key,
        model=settings.llm_model,
        fallback_model=settings.llm_fallback_model,
        max_output_tokens=settings.llm_max_output_tokens,
    )


def get_embedding_client() -> EmbeddingClient:
    return EmbeddingClient(
        api_key=settings.llm_api_key,
        model=settings.embedding_model,
        dimension=settings.embedding_dimension,
    )


def get_chunk_embedding_service() -> ChunkEmbeddingService:
    return ChunkEmbeddingService(get_embedding_client())
