from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

from app.domain import tag as ct
from app.crawler.detector import detect_language
from app.domain.news_entity import NewsEntity
from app.common.config.logging import logger

import re

def parse_link(html: str, content_tag: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    return [urljoin(base_url, a["href"]) for a in soup.select(content_tag)]

def fetch_link(html: str, link: str, organ: str) -> NewsEntity | None:
    soup = parse_html(html)
    title = extract_title(soup, ct.news_organ_extract_title_tag.get(organ))
    date = extract_date(soup, ct.news_organ_extract_date_tag.get(organ))
    soup = extract_contents(soup, ct.news_organ_extract_content_tag.get(organ))
    soup = decompose_contents_tag(soup, ct.removing_organ_tag.get(organ))
    soup = decompose_contents_text(soup, ct.removing_organ_text.get(organ))

    content = precleaning(soup)

    return NewsEntity(
        title=title,
        language=detect_language(content),
        content=content,
        url=link,
        created_at=convert_date_from_str(date, organ),
        crawled_at=datetime.now(),
        score=0
    )

def parse_html(html: str) -> str:
    return BeautifulSoup(html, "lxml")

def extract_title(soup: BeautifulSoup, tag: str) -> str:
    return soup.select_one(tag).get_text("\n", strip=True)

def extract_date(soup: BeautifulSoup, tag: str) -> str:
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

def convert_date_from_str(date: str, organ: str) -> datetime:
    result = ""

    if(organ == ct.NewsSource.YTN):
        dates = date.split()
        year_mon_day = dates[0][0:-1].split(".")
        year = year_mon_day[0]
        month = year_mon_day[1]
        day = year_mon_day[2]

        am_pm = 12 if dates[1] == "오후" else 0
        times = dates[2].split(":")
        hour = (int)(times[0]) + am_pm
        minute = times[1][0:-1]

        result = f"{year}-{month}-{day} {hour:02d}:{minute}"
    elif(organ == ct.NewsSource.YNA):
        ...
    elif(organ == ct.NewsSource.BBC):
        ...

    return datetime.strptime(result, "%Y-%m-%d %H:%M")