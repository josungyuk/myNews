from typing import Protocol
from app.domain.summary_entity import SummaryEntity

class SummaryRepositoryInterface(Protocol):
    def save(self, summary: SummaryEntity) -> bool: ...