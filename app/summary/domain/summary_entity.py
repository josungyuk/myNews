from datetime import datetime
from dataclasses import dataclass
from typing import Literal



@dataclass(frozen=False)
class SummaryEntity:
    id: int
    title: str
    importance_score: int

    summary: str
    reason: str
    key_points: list[str]
    keywords: list[str]
    category: str
    
    model_name: str
    prompt_version: str
    input_tokens: int
    output_tokens: int
    total_tokens: int

    created_at: datetime