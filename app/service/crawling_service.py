from selenium import webdriver
from app.common.config.logging import logger

from app.domain.parameter import parameters
from app.crawler.client import get_page_driver, driver_provider
from app.crawler.parser import parse_link, fetch_link
from app.repository.news_repository import NewsRepository


class CrawlingService:
    def __init__(self, repo: NewsRepository):
        self.repo = repo

    def fetch_latest(self) -> list:
        result = []

        with driver_provider() as driver:
            for param in parameters:
                news_organ = param[0]
                news_addr = param[1]
                page_id = param[2]
                content_tag = param[3]

                url = f"{news_addr}/{page_id}"

                html = get_page_driver(driver, url)
                links = parse_link(html, content_tag, url)[:1]

                for link in links:
                    article_html = get_page_driver(driver, link)
                    entity = fetch_link(article_html, link, news_organ)
                    if entity:
                        result.append(entity)
                        self.repo.save_ignore_duplicate(entity)

        return result