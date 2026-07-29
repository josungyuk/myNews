import json
from dataclasses import asdict
from datetime import datetime

from app.prompts.prompt_loader import PromptLoader
from app.llm.llm_client import LLMClient
from app.news.repository.news_repository import NewsRepository
from app.summary.repository.summary_repository import SummaryRepository
from app.news.domain.news_entity import NewsEntity

class SummaryService:
    def __init__(self, llm_client:LLMClient, news_repo: NewsRepository, summary_repo: SummaryRepository):
        self.llm_client = llm_client
        self.news_repo = news_repo
        self.summary_repo = summary_repo
        self.prompt_loader = PromptLoader()
    
    def summary_economy_priority(self, type: str) -> list:
        news:list[NewsEntity] = []

        if type == "economy":
            news = self.news_repo.read_economy_score_priority()
        elif type == "world":
            news = self.news_repo.read_world_score_priority()
        elif type == "total":
            news = self.news_repo.read_total_score_priority()

        news_json = self.news_entities_to_json(news)

        instructions = self.prompt_loader.load_instructions(type)
        prompt_template = f"""
            Analyze the following news data.

            {news_json}
        """

        response = self.llm_client.summarize(instuctions=instructions, prompt=prompt_template)

        return response

    def news_entities_to_json(self, news:list[NewsEntity]) -> list[dict]:
        data = [
            self.transform_to_json(news_entity)
            for news_entity in news
        ]

        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def transform_to_json(self, news: NewsEntity) -> str:
        data = asdict(news)

        if isinstance(data.get("created_at"), datetime):
            data["created_at"] = data["created_at"].isoformat()

        if isinstance(data.get("crawled_at"), datetime):
            data["crawled_at"] = data["crawled_at"].isoformat()

        data.pop("ids", None)
        data.pop("url", None)
        data.pop("crawled_at", None)

        return data
    