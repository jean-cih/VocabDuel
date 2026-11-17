from dataclasses import dataclass
from typing import Self
from copy import deepcopy


@dataclass
class DictStats:
    repetitions: int = 0
    average_comp: float = 0.0
    forgotten: int = 0
    known: int = 0

    def add_session(self, cards: int, forgotten: int, known: int) -> Self:
        new = deepcopy(self)

        new.repetitions += 1
        new.average_comp = int(100 - forgotten / cards * 100)
        new.forgotten += forgotten - known
        new.known += known - forgotten

        return new
