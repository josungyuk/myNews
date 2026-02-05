from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

from app.modules.news.infra.crawling.sources import tag as ct
from app.modules.news.infra.crawling.detector import detect_language
from app.modules.news.domain.entities.news_entity import NewsEntity
from app.common.config.logging import logger

import re

def parse_link(html: str, content_tag: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    return [urljoin(base_url, a["href"]) for a in soup.select(content_tag)]

def fetch_link(html: str, link: str, organ: str) -> NewsEntity | None:
    soup = parse_html(html)
    title = extract_title(soup, ct.new_organ_extract_title_tag.get(organ))
    soup = extract_contents(soup, ct.new_organ_extract_content_tag.get(organ))
    soup = decompose_contents_tag(soup, ct.removing_organ_tag.get(organ))
    soup = decompose_contents_text(soup, ct.removing_organ_text.get(organ))

    content = precleaning(soup)

    return NewsEntity(
        title=title,
        language=detect_language(content),
        content=content,
        url=link,
        created_at=datetime.now()
    )

def parse_html(html: str) -> str:
    return BeautifulSoup(html, "lxml")

def extract_title(soup: BeautifulSoup, tag: str) -> str:
    return soup.select_one(tag).get_text("\n", strip=True)

def extract_contents(soup: BeautifulSoup, tag: str) -> str:
    content = soup.select_one(tag)
    if not content:
        return None
    
    return content

def decompose_contents_tag(soup: BeautifulSoup, selector: list) -> str:
    for sel in selector:
        for tag in soup.select(sel):
            tag.decompose()

    return soup

def decompose_contents_text(soup: BeautifulSoup, selector: list) -> str:
    for keyword in selector:
        for text in soup.find_all(string=True):
            if text.strip().startswith(keyword):
                text.extract()

    return soup

def precleaning(soup: BeautifulSoup) -> str:
    results = []
    for p in soup.select("p"):
        text = p.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        if text:
            results.append(text)

    if not results:
        for p in soup.select("span"):
            text = p.get_text(" ", strip=True)
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                results.append(text)

    return "\n".join(results)