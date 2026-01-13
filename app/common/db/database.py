from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.common.config.settings import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping = True
)

session_local = sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush = False,
)