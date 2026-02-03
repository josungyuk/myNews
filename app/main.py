from fastapi import FastAPI
from app.modules.news.infra.api.router import router

from app.common.db.base import Base
from app.common.db.session_setting import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="News Service")

app.include_router(router)