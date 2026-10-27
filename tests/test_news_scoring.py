import json
import unittest
from datetime import datetime
from unittest.mock import patch

from app.news.domain.news_entity import NewsEntity
from app.news.service.news_service import CrawlingService


def make_entity(title: str, content: str) -> NewsEntity:
    return NewsEntity(
        url="https://example.com/news/1",
        type="world",
        source="bbc",
        title=title,
        content=content,
        language="en",
        created_at=datetime(2026, 10, 27, 10, 0),
        crawled_at=datetime(2026, 10, 27, 10, 1),
        world_score=0,
        economy_score=0,
        total_score=0,
        ids="",
    )


class NewsScoringTest(unittest.TestCase):
    def setUp(self):
        self.service = CrawlingService(None, None, None, None)

    @patch(
        "app.news.service.news_service.NEWS_KEYWORDS",
        {
            "economy": [{"id": "rates", "en": ["rate"]}],
            "world": [{"id": "war", "en": ["war"]}],
        },
    )
    def test_content_keyword_adds_one_point(self):
        result = self.service.score_news_keyword(make_entity("headline", "rate"))

        self.assertEqual(result.economy_score, 1)
        self.assertEqual(result.world_score, 0)
        self.assertEqual(result.total_score, 1)
        self.assertEqual(json.loads(result.keywords_id_scores), {"rates": 1})

    @patch(
        "app.news.service.news_service.NEWS_KEYWORDS",
        {
            "economy": [{"id": "rates", "en": ["rate"]}],
            "world": [{"id": "war", "en": ["war"]}],
        },
    )
    def test_title_keyword_adds_two_points(self):
        result = self.service.score_news_keyword(make_entity("rate", "headline"))

        self.assertEqual(result.economy_score, 2)
        self.assertEqual(result.total_score, 2)
        self.assertEqual(json.loads(result.keywords_id_scores), {"rates": 2})

    @patch(
        "app.news.service.news_service.NEWS_KEYWORDS",
        {
            "economy": [{"id": "rates", "en": ["rate"]}],
            "world": [{"id": "war", "en": ["war"]}],
        },
    )
    def test_title_and_content_scores_are_combined(self):
        result = self.service.score_news_keyword(make_entity("rate", "war rate"))

        self.assertEqual(result.economy_score, 3)
        self.assertEqual(result.world_score, 1)
        self.assertEqual(result.total_score, 4)
        self.assertEqual(json.loads(result.keywords_id_scores), {"rates": 3, "war": 1})

    @patch(
        "app.news.service.news_service.NEWS_KEYWORDS",
        {"economy": [], "world": []},
    )
    def test_article_without_keywords_has_zero_scores(self):
        result = self.service.score_news_keyword(make_entity("headline", "content"))

        self.assertEqual(result.economy_score, 0)
        self.assertEqual(result.world_score, 0)
        self.assertEqual(result.total_score, 0)
        self.assertEqual(result.keywords_id_scores, "{}")


if __name__ == "__main__":
    unittest.main()
