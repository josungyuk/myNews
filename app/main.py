from fastapi import FastAPI
from app.controller.crawling_controller import router as crawling_router
from app.controller.summary_controller import router as summary_router

from app.common.db.base import Base
from app.common.db.session_setting import engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="News Service")

app.include_router(crawling_router)
app.include_router(summary_router)