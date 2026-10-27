import unittest
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import TimeoutException

from app.common.config.tag import NewsSource, NewsType
from app.news.domain.news_entity import NewsEntity
from app.news.domain.result.news_score_result import NewsScoreResult
from app.news.service.news_service import CrawlingService


TEST_PARAMETER = (
    NewsSource.BBC,
    NewsType.WORLD,
    "https://example.com",
    "world",
    "a.article",
)


def make_entity(url: str) -> NewsEntity:
    return NewsEntity(
        url=url,
        type="",
        source="bbc",
        title="Headline",
        content="Article content",
        language="en",
        created_at=datetime(2026, 10, 27, 10, 0),
        crawled_at=datetime(2026, 10, 27, 10, 1),
        world_score=0,
        economy_score=0,
        total_score=0,
        ids="",
    )


class CrawlingServiceTest(unittest.TestCase):
    def setUp(self):
        self.repo = MagicMock()
        self.chunking = MagicMock()
        self.chunk_repo = MagicMock()
        self.embedding = MagicMock()
        self.service = CrawlingService(
            self.repo,
            self.chunking,
            self.chunk_repo,
            self.embedding,
        )
        self.service.score_news_keyword = MagicMock(
            return_value=NewsScoreResult(1, 0, 1, '{"keyword": 1}')
        )

    @patch("app.news.service.news_service.parse_link", return_value=[])
    @patch("app.news.service.news_service.get_page_driver")
    @patch("app.news.service.news_service.driver_provider")
    @patch("app.news.service.news_service.parameters", [TEST_PARAMETER])
    def test_empty_category_does_not_process_articles(
        self, driver_provider, get_page_driver, parse_link
    ):
        driver_provider.return_value.__enter__.return_value = object()
        get_page_driver.return_value = "category-html"

        result = self.service.fetch_latest()

        self.assertEqual(result, [])
        self.repo.save_ignore_duplicate.assert_not_called()

    @patch("app.news.service.news_service.fetch_link")
    @patch("app.news.service.news_service.parse_link", return_value=["https://example.com/1"])
    @patch("app.news.service.news_service.get_page_driver")
    @patch("app.news.service.news_service.driver_provider")
    @patch("app.news.service.news_service.parameters", [TEST_PARAMETER])
    def test_successful_article_is_saved_and_chunked(
        self, driver_provider, get_page_driver, parse_link, fetch_link
    ):
        driver_provider.return_value.__enter__.return_value = object()
        get_page_driver.side_effect = ["category-html", "article-html"]
        entity = make_entity("https://example.com/1")
        fetch_link.return_value = entity
        self.repo.save_ignore_duplicate.return_value = 101
        chunks = [SimpleNamespace(news_id=101)]
        self.chunking.chunk.return_value = chunks
        self.embedding.embed.return_value = chunks

        result = self.service.fetch_latest()

        self.assertEqual(result, [entity])
        self.repo.save_ignore_duplicate.assert_called_once_with(entity)
        self.chunking.chunk.assert_called_once_with(
            news_id=101,
            content=entity.content,
        )
        self.embedding.embed.assert_called_once_with(chunks)
        self.chunk_repo.save_all.assert_called_once_with(chunks)
        self.repo.commit.assert_called_once_with()
        self.repo.rollback.assert_not_called()

    @patch("app.news.service.news_service.fetch_link")
    @patch("app.news.service.news_service.parse_link", return_value=["https://example.com/1"])
    @patch("app.news.service.news_service.get_page_driver")
    @patch("app.news.service.news_service.driver_provider")
    @patch("app.news.service.news_service.parameters", [TEST_PARAMETER])
    def test_duplicate_is_not_chunked(
        self, driver_provider, get_page_driver, parse_link, fetch_link
    ):
        driver_provider.return_value.__enter__.return_value = object()
        get_page_driver.side_effect = ["category-html", "article-html"]
        fetch_link.return_value = make_entity("https://example.com/1")
        self.repo.save_ignore_duplicate.return_value = None

        self.assertEqual(self.service.fetch_latest(), [])
        self.chunking.chunk.assert_not_called()
        self.embedding.embed.assert_not_called()
        self.chunk_repo.save_all.assert_not_called()
        self.repo.rollback.assert_called_once_with()

    @patch("app.news.service.news_service.fetch_link", side_effect=[None, make_entity("https://example.com/2")])
    @patch(
        "app.news.service.news_service.parse_link",
        side_effect=[["https://example.com/1"], ["https://example.com/2"]],
    )
    @patch("app.news.service.news_service.get_page_driver")
    @patch("app.news.service.news_service.driver_provider")
    @patch("app.news.service.news_service.parameters", [TEST_PARAMETER, TEST_PARAMETER])
    def test_parser_failure_does_not_stop_next_article(
        self, driver_provider, get_page_driver, parse_link, fetch_link
    ):
        driver_provider.return_value.__enter__.return_value = object()
        get_page_driver.side_effect = [
            "category-html",
            "failed-html",
            "category-html",
            "success-html",
        ]
        self.repo.save_ignore_duplicate.return_value = 102
        chunks = [SimpleNamespace(news_id=102)]
        self.chunking.chunk.return_value = chunks
        self.embedding.embed.return_value = chunks

        result = self.service.fetch_latest()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].url, "https://example.com/2")
        self.assertEqual(self.repo.save_ignore_duplicate.call_count, 1)

    @patch("app.news.service.news_service.fetch_link", return_value=make_entity("https://example.com/2"))
    @patch(
        "app.news.service.news_service.parse_link",
        side_effect=[["https://example.com/1"], ["https://example.com/2"]],
    )
    @patch("app.news.service.news_service.get_page_driver")
    @patch("app.news.service.news_service.driver_provider")
    @patch("app.news.service.news_service.parameters", [TEST_PARAMETER, TEST_PARAMETER])
    def test_timeout_does_not_stop_next_article(
        self, driver_provider, get_page_driver, parse_link, fetch_link
    ):
        driver_provider.return_value.__enter__.return_value = object()
        get_page_driver.side_effect = [
            "category-html",
            TimeoutException("timed out"),
            "category-html",
            "success-html",
        ]
        self.repo.save_ignore_duplicate.return_value = 103
        chunks = [SimpleNamespace(news_id=103)]
        self.chunking.chunk.return_value = chunks
        self.embedding.embed.return_value = chunks

        result = self.service.fetch_latest()

        self.assertEqual(len(result), 1)
        self.assertEqual(fetch_link.call_count, 1)

    @patch("app.news.service.news_service.fetch_link", return_value=make_entity("https://example.com/1"))
    @patch("app.news.service.news_service.parse_link", return_value=["https://example.com/1"])
    @patch("app.news.service.news_service.get_page_driver")
    @patch("app.news.service.news_service.driver_provider")
    @patch("app.news.service.news_service.parameters", [TEST_PARAMETER])
    def test_embedding_failure_still_saves_chunks(
        self, driver_provider, get_page_driver, parse_link, fetch_link
    ):
        driver_provider.return_value.__enter__.return_value = object()
        get_page_driver.side_effect = ["category-html", "article-html"]
        self.repo.save_ignore_duplicate.return_value = 104
        chunks = [SimpleNamespace(news_id=104)]
        self.chunking.chunk.return_value = chunks
        self.embedding.embed.side_effect = RuntimeError("embedding unavailable")

        result = self.service.fetch_latest()

        self.assertEqual(len(result), 1)
        self.chunk_repo.save_all.assert_called_once_with(chunks)
        self.repo.commit.assert_called_once_with()

    @patch(
        "app.news.service.news_service.fetch_link",
        side_effect=[
            make_entity("https://example.com/1"),
            make_entity("https://example.com/2"),
        ],
    )
    @patch(
        "app.news.service.news_service.parse_link",
        side_effect=[["https://example.com/1"], ["https://example.com/2"]],
    )
    @patch("app.news.service.news_service.get_page_driver")
    @patch("app.news.service.news_service.driver_provider")
    @patch("app.news.service.news_service.parameters", [TEST_PARAMETER, TEST_PARAMETER])
    def test_database_failure_rolls_back_before_next_article(
        self, driver_provider, get_page_driver, parse_link, fetch_link
    ):
        driver_provider.return_value.__enter__.return_value = object()
        get_page_driver.side_effect = [
            "category-html",
            "failed-article-html",
            "category-html",
            "successful-article-html",
        ]
        self.repo.save_ignore_duplicate.side_effect = [201, 202]
        self.chunking.chunk.side_effect = [
            [SimpleNamespace(news_id=201)],
            [SimpleNamespace(news_id=202)],
        ]
        self.embedding.embed.side_effect = lambda chunks: chunks
        self.chunk_repo.save_all.side_effect = [RuntimeError("database error"), None]

        result = self.service.fetch_latest()

        self.assertEqual([entity.url for entity in result], ["https://example.com/2"])
        self.repo.rollback.assert_called_once_with()
        self.repo.commit.assert_called_once_with()

    @patch(
        "app.news.service.news_service.fetch_link",
        return_value=make_entity("https://example.com/1"),
    )
    @patch(
        "app.news.service.news_service.parse_link",
        return_value=["https://example.com/1"],
    )
    @patch("app.news.service.news_service.get_page_driver")
    @patch("app.news.service.news_service.driver_provider")
    @patch("app.news.service.news_service.parameters", [TEST_PARAMETER])
    def test_commit_failure_rolls_back_current_article(
        self, driver_provider, get_page_driver, parse_link, fetch_link
    ):
        driver_provider.return_value.__enter__.return_value = object()
        get_page_driver.side_effect = ["category-html", "article-html"]
        self.repo.save_ignore_duplicate.return_value = 203
        chunks = [SimpleNamespace(news_id=203)]
        self.chunking.chunk.return_value = chunks
        self.embedding.embed.return_value = chunks
        self.repo.commit.side_effect = RuntimeError("commit failed")

        result = self.service.fetch_latest()

        self.assertEqual(result, [])
        self.repo.rollback.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
