import unittest
from datetime import datetime

from app.common.config.tag import NewsSource
from app.crawler.parser import (
    convert_date_from_str,
    fetch_link,
    parse_link,
    precleaning,
    parse_html,
)


class CrawlerParserTest(unittest.TestCase):
    def test_parse_link_makes_relative_url_absolute(self):
        html = '<a class="article" href="/news/1">Article</a>'

        links = parse_link(html, "a.article", "https://example.com/list")

        self.assertEqual(links, ["https://example.com/news/1"])

    def test_precleaning_uses_paragraphs_before_spans(self):
        soup = parse_html(
            "<div><span>fallback</span><p> first  text </p><p></p></div>"
        )

        self.assertEqual(precleaning(soup), "first text")

    def test_precleaning_uses_spans_when_paragraphs_are_absent(self):
        soup = parse_html("<div><span> first  text </span></div>")

        self.assertEqual(precleaning(soup), "first text")

    def test_fetch_link_returns_valid_bbc_entity(self):
        html = """
        <div data-component="headline-block">Test headline</div>
        <time datetime="2026-10-27T10:00:00.000Z"></time>
        <article><p>Article content</p></article>
        """

        entity = fetch_link(html, "https://bbc.example/news/1", NewsSource.BBC)

        self.assertIsNotNone(entity)
        self.assertEqual(entity.title, "Test headline")
        self.assertEqual(entity.content, "Article content")
        self.assertEqual(entity.source, "bbc")

    def test_fetch_link_returns_none_when_required_data_is_missing(self):
        cases = [
            "<html></html>",
            '<div data-component="headline-block">Headline</div>',
            """
            <div data-component="headline-block">Headline</div>
            <time datetime="2026-10-27T10:00:00.000Z"></time>
            """,
            """
            <div data-component="headline-block">Headline</div>
            <time datetime="2026-10-27T10:00:00.000Z"></time>
            <article><div>no paragraphs or spans</div></article>
            """,
        ]

        for html in cases:
            with self.subTest(html=html):
                self.assertIsNone(
                    fetch_link(html, "https://bbc.example/news/1", NewsSource.BBC)
                )

    def test_date_conversion_for_supported_publishers(self):
        cases = [
            (NewsSource.YNA, "2026-10-27 10:20", datetime(2026, 10, 27, 10, 20)),
            (
                NewsSource.BBC,
                "2026-10-27T10:20:00.000Z",
                datetime(2026, 10, 27, 19, 20),
            ),
            (
                NewsSource.GUARDIAN,
                "Monday 27 Oct 2026 10:20 GMT",
                datetime(2026, 10, 27, 19, 20),
            ),
            (
                NewsSource.NPR,
                "2026-10-27T10:20:00+00:00",
                datetime(2026, 10, 27, 19, 20),
            ),
        ]

        for organ, raw_date, expected in cases:
            with self.subTest(organ=organ):
                self.assertEqual(convert_date_from_str(raw_date, organ), expected)


if __name__ == "__main__":
    unittest.main()
