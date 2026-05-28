from typing import Protocol
from app.summary.domain.summary_entity import SummaryEntity

class SummaryRepositoryInterface(Protocol):
    def save(self, summary: SummaryEntity) -> bool: ...