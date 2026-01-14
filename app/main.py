from fastapi import FastAPI
from app.modules.news.infra.api import router as news_router

app = FastAPI(title="News Service")

app.include_router(news_router)