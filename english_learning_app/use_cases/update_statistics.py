from english_learning_app.domain.knowledge_statistic import KnowledgeStats
from english_learning_app.ports.stats_repository import StatsRepository


def update_statistics(
    stat_repo: StatsRepository,
    path: str,
    cards: int,
    forgot: int = 0,
    learnt: int = 0,
    topic: str = "",
    max_topic: int = 0,
) -> None:
    stats = stat_repo.load(path)
    new_stats = stats.add_session(cards, forgot, learnt, topic, max_topic)
    stat_repo.save(path, new_stats)
