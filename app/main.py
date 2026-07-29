from fastapi import FastAPI
from app.news.controller.news_controller import router as news_router
from app.summary.controller.summary_controller import router as summary_router

app = FastAPI(title="News Service")

app.include_router(news_router)
app.include_router(summary_router)