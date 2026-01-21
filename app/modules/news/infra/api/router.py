from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.modules.news.application.usecase.crawling import Crawling
from app.modules.news.infra.crawling.client import driver_provider

router = APIRouter()

@router.get("/news")
def get_news():
    """
    Docstring for get_news
    """

    crawling = Crawling()

    with driver_provider() as driver:
      results = crawling.fetch_latest(driver)
      
    return results