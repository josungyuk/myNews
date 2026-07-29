from bs4 import (BeautifulSoup, Tag)
from datetime import datetime
from urllib.parse import urljoin
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

from app.common.config import tag as ct
from app.crawler.detector import detect_language
from app.news.domain.news_entity import NewsEntity
from app.common.config.logging import logger

import re

def parse_link(html: str, content_tag: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    return [urljoin(base_url, a["href"]) for a in soup.select(content_tag)]

def fetch_link(html: str, link: str, organ: ct.NewsSource) -> NewsEntity | None:
    logger.info(link)
    soup = parse_html(html)

    title = extract_title(soup, ct.news_organ_extract_title_tag.get(organ))

    if title is None:
        logger.warning(
            "Title not found: source=%s url=%s",
            organ.value,
            link,
        )
        return None

    date = extract_date(soup, ct.news_organ_extract_date_tag.get(organ), ct.news_organ_date_tag_value.get(organ))

    if date is None:
        logger.warning(
            "Publication date not found: source:%s url:%s",
            organ.value,
            link,
        )
        return None

    content_soup = extract_contents(soup, ct.news_organ_extract_content_tag.get(organ))

    if content_soup is None:
        logger.warning(
                    "Content container not found: source=%s url=%s",
                    organ.value,
                    link,
                )
        return None

    content_soup = decompose_contents_tag(content_soup, ct.removing_organ_tag.get(organ))
    content_soup = decompose_contents_text(content_soup, ct.removing_organ_text.get(organ))

    content = precleaning(content_soup)

    if not content.strip():
        logger.warning(
            "Article content is empty: source=%s, url=%s",
            organ.value,
            link,
        )
        return None
    
    return NewsEntity(
        url=link,
        type="",
        source=organ.value,
        title=title,
        content=content,
        language=ct.news_language.get(organ),
        created_at=convert_date_from_str(date, organ),
        crawled_at=datetime.now(),
        economy_score=0,
        world_score=0,
        total_score=0,
        ids=""
    )

def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")

def extract_title(soup: BeautifulSoup, tag: str) -> str | None:
    element = soup.select_one(tag)

    if element is None:
        return None

    title = element.get_text(" ", strip=True)

    return title or None

def extract_date(soup: BeautifulSoup, tag: str, tag_value: str | None) -> str | None:
    element = soup.select_one(tag)

    if element is None:
        return None

    if tag_value:
        date = element.get(tag_value)
    else:
        date = element.get_text(" ", strip=True)

    return date or None

def extract_contents(soup: BeautifulSoup, tag: str) -> Tag | None:
    content = soup.select_one(tag)

    if not content:
        return None
    
    return content

def decompose_contents_tag(soup: Tag, selector: list[str]) -> Tag:
    for sel in selector:
        for tag in soup.select(sel):
            tag.decompose()

    return soup

def decompose_contents_text(soup: Tag, selector: list[str]) -> Tag:
    for keyword in selector:
        for text in soup.find_all(string=True):
            if text.strip().startswith(keyword):
                text.extract()

    return soup

def precleaning(soup: Tag) -> str:
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

def convert_date_from_str(date: str, organ: ct.NewsSource) -> datetime:
    result = ""

    if(organ == ct.NewsSource.YTN):
        dates = date.split()
        year_mon_day = dates[0][0:-1].split(".")
        year = year_mon_day[0]
        month = year_mon_day[1]
        day = year_mon_day[2]

        period = dates[1]
        
        times = dates[2].split(":")
        hour = int(times[0])
        minute = times[1].rstrip(".분")

        if period == "오전" and hour == 12:
            hour = 0
        elif period == "오후" and hour != 12:
            hour += 12

        result = f"{year}-{month}-{day} {hour:02d}:{minute}"
    elif(organ == ct.NewsSource.YNA):
        result = date
    elif(organ == ct.NewsSource.BBC):
        dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        dt = dt.replace(tzinfo=timezone.utc)

        kst = dt.astimezone(timezone(timedelta(hours=9)))

        result = kst.strftime("%Y-%m-%d %H:%M")
    elif(organ == ct.NewsSource.GUARDIAN):
        dates = date.split(" ")
        result = convert_guarians_to_date(dates[1], dates[2], dates[3], dates[4])
    elif(organ == ct.NewsSource.NPR):
        dt = datetime.fromisoformat(date)
        kst_dt = dt.astimezone(ZoneInfo("Asia/Seoul"))

        result = kst_dt.strftime("%Y-%m-%d %H:%M")

    return datetime.strptime(result, "%Y-%m-%d %H:%M")

def convert_guarians_to_date(day: int, month: str, year: int, time: str) -> str:
    month_dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }

    month = month_dict.get(month)
    hour = (int)(time[0:2])
    minute = time[3:5]

    formatted_date = f"{year}-{month}-{day} {hour:02d}:{minute}"

    dt = datetime.strptime(formatted_date, "%Y-%m-%d %H:%M")
    dt = dt.replace(tzinfo=ZoneInfo("Europe/London"))
    kst = dt.astimezone(ZoneInfo("Asia/Seoul"))

    result = datetime.strftime(kst, "%Y-%m-%d %H:%M")

    return result