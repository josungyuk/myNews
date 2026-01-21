from typing import Protocol
from selenium import webdriver

class CrawlingPort(Protocol):
    def fetch_latest(self, driver: webdriver, news_organ: str, homepage_addr: str, page_id: str, content_tag: str) -> tuple:
        ...