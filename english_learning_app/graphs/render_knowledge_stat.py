from english_learning_app.domain.knowledge_statistic import KnowledgeStats

# Политра
COLOR_CARDS = "rgba(32, 237, 132)"
COLOR_FORGOTTEN = "rgba(255, 94, 0)"
COLOR_TOPICS = "rgba(109, 40, 217)"
COLOR_GOAL = "rgba(32, 237, 132, 0.6)"
COLOR_BACK_GOAL = "rgba(0, 0, 0, 0)"


def render(stats: KnowledgeStats) -> str:

    content = render_cards_per_day(stats)

    content += render_knowledge(stats)

    content += render_topics(stats)

    content += render_string_stat(stats)

    return content


def render_cards_per_day(stats: KnowledgeStats) -> str:
    content = "\n### Cards completed per day\n"

    content += "```chart\ntype: bar\nlabels: ["
    content += ", ".join(str(label) for label in stats.get_time_labels())

    content += "]\nseries:\n  - label: Words per day\n    data: ["
    content += ", ".join(str(cards) for cards in stats.cards_per_day)

    content += f"]\n    backgroundColor: {COLOR_CARDS}\n```\n"
    return content


def render_knowledge(stats: KnowledgeStats) -> str:
    content = "\n### Current level of knowledge\n"

    content += "```chart\ntype: bar\nlabels: ["
    content += ", ".join(str(label) for label in stats.get_time_labels())

    content += "]\nseries:\n  - label: Forgot / New\n    data: ["
    content += ", ".join(str(forgotten) for forgotten in stats.forgotten_per_day)

    content += f"]\n    backgroundColor: {COLOR_FORGOTTEN}\n"

    content += "  - label: Know\n    data: ["
    content += ", ".join(str(known) for known in stats.known_per_day)

    content += f"]\n    backgroundColor: {COLOR_CARDS}\n```\n"

    return content


def render_topics(stats: KnowledgeStats) -> str:
    content = "\n### Progress on Topics\n"

    content += "```chart\ntype: line\nlabels: ["
    content += ", ".join(topic for topic in stats.topics.keys())

    content += "]\nseries:\n  - label: (%)\n    data: ["
    content += ", ".join(str(value) for _, value in stats.topics.items())

    content += f"]\n    backgroundColor: {COLOR_TOPICS}"
    content += f"\n    borderColor: {COLOR_CARDS}"
    content += f"\n    pointBackgroundColor: {COLOR_CARDS}"
    content += f"\n    fill: true"

    content += "\n  - label: 'Goal: 100%'\n    data: ["
    content += ", ".join("100" for _ in range(len(stats.topics)))

    content += f"]\n    backgroundColor: {COLOR_BACK_GOAL}"
    content += f"\n    borderColor: {COLOR_GOAL}"
    content += f"\n    borderDash: [8, 4]"
    content += f"\n    pointRadius: 0"
    content += f"\n    fill: true"
    content += f"\n    borderWidth: 2\n```"

    return content


def render_string_stat(stats: KnowledgeStats) -> str:
    return (
        f"\n**Total number of cards for all time: {stats.get_cards_for_all_time()}\n\n"
        f"**Total number of all words: {stats.get_all_words()}\n\n"
        f"**Total number of known words: {stats.get_known_words()}🔥\n\n"
        f"**Setup Date: {stats.setup_date}\n\n"
        f"**Last Entry: {stats.last_entry}\n"
    )
