from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=False)
class NewsEntity:
    url: str
    title: str
    content: str
    created_at: datetime
