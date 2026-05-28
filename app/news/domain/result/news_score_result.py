from dataclasses import dataclass

@dataclass(frozen=True)
class NewsScoreResult:
    world_score: int
    economy_score: int
    total_score: int
    keywords_id_scores: str