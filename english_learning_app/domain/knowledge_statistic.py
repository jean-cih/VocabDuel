from datetime import date
from dataclasses import field, dataclass
from typing import Self
from copy import deepcopy


@dataclass
class KnowledgeStats:
    setup_date: date
    last_entry: date
    cards_per_day: list[int] = field(default_factory=list)
    forgotten_per_day: list[int] = field(default_factory=list)
    known_per_day: list[int] = field(default_factory=list)
    topics: dict[str, int] = field(default_factory=dict)

    def get_time_labels(self) -> list[int]:
        return list(range(1, len(self.cards_per_day)))

    def get_cards_for_all_time(self) -> int:
        return sum(self.cards_per_day)

    def get_all_words(self) -> int:
        return self.forgotten_per_day[-2] + self.known_per_day[-2]

    def get_known_words(self) -> int:
        return self.known_per_day[-2]

    def get_forgotten_words(self) -> int:
        return self.forgotten_per_day[-2]

    def add_session(
        self,
        cards: int,
        forgot: int = 0,
        learnt: int = 0,
        topic: str = "",
        max_topic: int = 0,
    ) -> Self:
        new = deepcopy(self)
        today = date.today()

        diff = today - new.last_entry
        days = diff.days
        if days > 0:
            forgotten = new.forgotten_per_day[-2]
            known = new.known_per_day[-2]

            new.forgotten_per_day[-1] = forgotten
            new.known_per_day[-1] = known

            for i in range(days):
                new.cards_per_day.append(0)
                new.forgotten_per_day.append(forgotten)
                new.known_per_day.append(known)

            new.cards_per_day[-2] = cards

            new.forgotten_per_day[-2] += forgot - learnt
            new.forgotten_per_day[-1] = 0

            new.known_per_day[-2] += learnt - forgot
            new.known_per_day[-1] = 0
        else:
            new.cards_per_day[-2] += cards
            new.forgotten_per_day[-2] += forgot - learnt
            new.known_per_day[-2] += learnt - forgot
        new.last_entry = today

        if topic != "" and f"'{topic}'" not in new.topics:
            new.topics[f"'{topic}'"] = int((learnt - forgot) / max_topic * 100)
        elif topic != "":
            new_current_know_topic = (
                new.topics[f"'{topic}'"] * max_topic / 100 + learnt - forgot
            )
            new.topics[f"'{topic}'"] = int(new_current_know_topic / max_topic * 100)

        return new
