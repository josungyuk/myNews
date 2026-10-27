import json
import unittest
from datetime import datetime
from unittest.mock import MagicMock

from app.news.domain.news_entity import NewsEntity
from app.summary.service.summary_service import SummaryService


def make_entity() -> NewsEntity:
    return NewsEntity(
        url="https://example.com/news/1",
        type="world",
        source="bbc",
        title="Headline",
        content="Content",
        language="en",
        created_at=datetime(2026, 10, 27, 10, 0),
        crawled_at=datetime(2026, 10, 27, 10, 1),
        world_score=1,
        economy_score=2,
        total_score=3,
        ids='{"keyword": 1}',
    )


class SummaryServiceTest(unittest.TestCase):
    def setUp(self):
        self.llm = MagicMock()
        self.news_repo = MagicMock()
        self.summary_repo = MagicMock()
        self.service = SummaryService(self.llm, self.news_repo, self.summary_repo)
        self.service.prompt_loader = MagicMock()
        self.service.prompt_loader.load_instructions.return_value = "instructions"
        self.llm.summarize.return_value = {"summary": "result"}

    def test_economy_uses_economy_priority_news(self):
        self.news_repo.read_economy_score_priority.return_value = [make_entity()]

        result = self.service.summary_economy_priority("economy")

        self.news_repo.read_economy_score_priority.assert_called_once_with()
        self.assertEqual(result, {"summary": "result"})
        self.service.prompt_loader.load_instructions.assert_called_once_with("economy")

    def test_world_and_total_use_their_priority_queries(self):
        self.news_repo.read_world_score_priority.return_value = []
        self.news_repo.read_total_score_priority.return_value = []

        self.service.summary_economy_priority("world")
        self.service.summary_economy_priority("total")

        self.news_repo.read_world_score_priority.assert_called_once_with()
        self.news_repo.read_total_score_priority.assert_called_once_with()

    def test_summary_prompt_contains_serialized_news(self):
        self.news_repo.read_economy_score_priority.return_value = [make_entity()]

        self.service.summary_economy_priority("economy")

        prompt = self.llm.summarize.call_args.kwargs["prompt"]
        serialized = json.loads(prompt.split("Analyze the following news data.", 1)[1])
        self.assertEqual(serialized[0]["title"], "Headline")
        self.assertNotIn("url", serialized[0])
        self.assertNotIn("ids", serialized[0])
        self.assertNotIn("crawled_at", serialized[0])
        self.assertEqual(serialized[0]["created_at"], "2026-10-27T10:00:00")

    def test_transform_to_json_removes_non_summary_fields(self):
        result = self.service.transform_to_json(make_entity())

        self.assertEqual(result["created_at"], "2026-10-27T10:00:00")
        self.assertNotIn("url", result)
        self.assertNotIn("ids", result)
        self.assertNotIn("crawled_at", result)


if __name__ == "__main__":
    unittest.main()
