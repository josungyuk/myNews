from selenium import webdriver
from app.common.config.logging import logger

from app.modules.news.infra.crawling.sources.parameter import parameters
from app.modules.news.application.interface.crawling_port import CrawlingPort
from app.modules.news.infra.crawling.client import get_page_driver
from app.modules.news.infra.crawling.parser import parse_link, fetch_link
from app.modules.news.infra.repositories.news_repository import NewsRepository


class Crawling(CrawlingPort):
    def __init__(self, repo: NewsRepository):
        self.repo = repo

    def fetch_latest(self, driver: webdriver) -> list:
        result = []
        for param in parameters:
            news_organ = param[0]
            news_addr = param[1]
            page_id = param[2]
            content_tag = param[3]

            url = f"{news_addr}/{page_id}"

            html = get_page_driver(driver, url)
            links = parse_link(html, content_tag, url)[:10]

            logger.info(links)

            for link in links:
                article_html = get_page_driver(driver, link)
                entity = fetch_link(article_html, link, news_organ)
                if entity:
                    self.repo.save(entity)

        return result