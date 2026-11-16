from typing import Protocol
from english_learning_app.domain.knowledge_statistic import KnowledgeStats


class StatsRepository(Protocol):
    def load(self, path: str) -> KnowledgeStats: ...
    def save(self, path: str, stats: KnowledgeStats) -> None: ...
