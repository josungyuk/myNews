from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.common.config.settings import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping = True
)

SessionLocal = sessionmaker(
    bind = engine,
    autocommit = False,
    autoflush = False,
)

def get_session() -> Session:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()