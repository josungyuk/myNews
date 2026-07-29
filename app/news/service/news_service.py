import json

from collections import Counter

from selenium import webdriver
from app.common.config.logging import logger
from selenium.common.exceptions import (TimeoutException, WebDriverException)

from app.common.config.parameter import parameters
from app.crawler.client import get_page_driver, driver_provider
from app.crawler.parser import parse_link, fetch_link
from app.news.repository.news_repository import NewsRepository
from app.news.domain.news_entity import NewsEntity
from app.news.domain.result.news_score_result import NewsScoreResult
from app.common.config.news_keyword import NEWS_KEYWORDS
from app.common.config.tag import NewsType



class CrawlingService:
    def __init__(self, repo: NewsRepository):
        self.repo = repo

    def fetch_latest(self) -> list:
        result = []
        counts = 10

        
        for param in parameters:
            news_organ = param[0]
            news_type = param[1]
            news_addr = param[2]
            page_id = param[3]
            content_tag = param[4]

            url = f"{news_addr}/{page_id}"

            try:
                with driver_provider() as driver:

                    html = get_page_driver(driver, url)
                    links = parse_link(html, content_tag, url)[:counts]

            

                    for link in links:
                        try:
                            article_html = get_page_driver(driver, link)
                            entity = fetch_link(article_html, link, news_organ)

                            if entity is None:
                                logger.warning(
                                    "Skipping article because parsing failed: %s",
                                    link
                                )
                                continue

                            
                            entity.type = news_type.value
                            id_score = self.score_news_keyword(entity)
                            entity.economy_score = id_score.economy_score
                            entity.world_score = id_score.world_score
                            entity.total_score = id_score.total_score
                            entity.ids = id_score.keywords_id_scores
                            
                            created = self.repo.save_ignore_duplicate(entity)

                            if created:
                                result.append(entity)

                        except TimeoutException:
                            logger.warning("Page timed out: %s", link)
                            continue

                        except WebDriverException:
                            logger.exception("Browser failed while loading: %s", link)
                            break

                        except Exception:
                            logger.warning(
                                "Faild to process article: source:%s category=%s url=%s",
                                news_organ.value,
                                news_type.value,
                                link,
                            )
                            continue
            except TimeoutException:
                logger.warning("Category page timed out: source=%s category=%s url=%s",
                    news_organ.value,
                    news_type.value,
                    url,
                )
                continue

            except WebDriverException:
                logger.exception("Browser failed while processing category: source=%s category=%s url=%s",
                    news_organ.value,
                    news_type.value,
                    url,
                )
                continue

            except Exception:
                logger.exception("Failed to process category: source=%s category=%s url=%s",
                    news_organ.value,
                    news_type.value,
                    url,
                )
                continue

        return result
    
    def score_news_keyword(self, entity: NewsEntity) -> NewsScoreResult:
        language = entity.language
        title = entity.title.lower()
        content = entity.content.lower()

        total_score = 0
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
