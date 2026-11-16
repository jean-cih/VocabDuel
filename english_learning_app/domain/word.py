from dataclasses import dataclass
import re
from typing import Self


@dataclass
class Word:
    number: int
    english: str
    russian: str
    u: int
    f: int
    known: bool = False

    _RE = re.compile(
        r"(\d+)\.\s*"
        r"(?:_\(🤯F\s*-\s*(\d+);\s*🧠U\s*-\s*(\d+)\)_)?\s*"
        r"(🔥)?\*\*([^*]+)\*\*\s*[-–—]\s*(.+?)\s*$"
    )

    @classmethod
    def parse(cls, line: str) -> Self | None:
        m = cls._RE.match(line.strip())
        if not m:
            return None
        number, f, u, fire, eng, rus = m.groups()
        return cls(
            number=int(number),
            english=eng.strip(),
            russian=rus.strip(),
            u=int(u) if u is not None else 0,
            f=int(f) if f is not None else 0,
            known=bool(fire),
        )

    def render(self) -> str:
        fire = "🔥" if self.known else ""
        stats = f"_(🤯F - {self.f}; 🧠U - {self.u})_"
        return f"{self.number}. {stats} {fire}**{self.english}** - {self.russian}"
