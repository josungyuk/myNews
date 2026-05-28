from app.common.config.settings import settings
from app.llm.llm_client import LLMClient


def get_llm_client() -> LLMClient:
    return LLMClient(
        api_key=settings.llm_api_key,
        model=settings.llm_model
    )