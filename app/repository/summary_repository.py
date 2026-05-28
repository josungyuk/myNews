from app.common.db.session_setting import Session

class SummaryRepository:
    def __init__(self, session: Session):
        self._session = session

    