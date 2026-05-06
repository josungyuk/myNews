import json

from collections import Counter

from selenium import webdriver
from app.common.config.logging import logger

from app.common.config.parameter import parameters
from app.crawler.client import get_page_driver, driver_provider
from app.crawler.parser import parse_link, fetch_link
from app.repository.news_repository import NewsRepository
from app.domain.news_entity import NewsEntity
from app.domain.result.news_score_result import NewsScoreResult
from app.common.config.new_keyword import NEWS_KEYWORDS
from app.common.config.tag import NewsType


class CrawlingService:
    def __init__(self, repo: NewsRepository):
        self.repo = repo

    def fetch_latest(self) -> list:
        result = []
        counts = 10

        with driver_provider() as driver:
            for param in parameters:
                news_organ = param[0]
                news_type = param[1]
                news_addr = param[2]
                page_id = param[3]
                content_tag = param[4]

                url = f"{news_addr}/{page_id}"

                html = get_page_driver(driver, url)
                links = parse_link(html, content_tag, url)[:counts]

                for link in links:
                    article_html = get_page_driver(driver, link)
                    entity = fetch_link(article_html, link, news_organ)
                    if entity:
                        entity.type = news_type.value
                        id_score = self.score_news_keyword(entity)
                        entity.economy_score = id_score.economy_score
                        entity.world_score = id_score.world_score
                        entity.total_score = id_score.total_score
                        entity.ids = id_score.keywords_id_scores
                        result.append(entity)
                        self.repo.save_ignore_duplicate(entity)

        return result
    
    def score_news_keyword(self, entity: NewsEntity) -> NewsScoreResult:
        language = entity.language
        title = entity.title.lower()
        content = entity.content.lower()

        total_score = 0;
        counter = Counter()

        economy_score = 0
        match_keywords = NEWS_KEYWORDS[NewsType.ECONOMY.value]
        for keyword in match_keywords:
            concept_id = keyword["id"]
            aliases = keyword[language]

            for aliase in aliases:
                if aliase.lower() in content:
                    economy_score += 1
                    counter[concept_id] += 1
                

            for aliase in aliases:
                if aliase.lower() in title:
                    economy_score += 2
                    counter[concept_id] += 2

        world_score = 0
        match_keywords = NEWS_KEYWORDS[NewsType.WORLD.value]
        for keyword in match_keywords:
            concept_id = keyword["id"]
            aliases = keyword[language]

            for aliase in aliases:
                if aliase.lower() in content:
                    world_score += 1
                    counter[concept_id] += 1
                

            for aliase in aliases:
                if aliase.lower() in title:
                    world_score += 2
                    counter[concept_id] += 2

        total_score = economy_score + world_score

        keyword_id_scores = json.dumps(dict(counter))

        return NewsScoreResult(
            world_score= world_score,
            economy_score= economy_score,
            total_score= total_score,
            keywords_id_scores= keyword_id_scores
        )
    


# + 뉴스를 국제뉴스를 기반으로 할건지, 사회뉴스를 기반으로 할건지 정해야함. 초기 구상은 사회였으나 현재 구상은 국제임
# + 고로 국제뉴스로 수정하려면 YTN, YNA, BBC 사회 항목을 world로 변경해야함.