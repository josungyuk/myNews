from fastapi import FastAPI
from app.modules.news.infra.api.router import router

app = FastAPI(title="News Service")

app.include_router(router)