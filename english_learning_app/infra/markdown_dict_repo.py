import os
import re

from english_learning_app.domain.dict_statistic import DictStats
from english_learning_app.domain.word import Word
from english_learning_app.graphs.render_dict_stat import render_dict_stat


class MarkdownDictRepository:
    def load(self, path: str) -> list[Word]:
        words = []
        for filepath in self._list_files(path):
            with open(filepath, "r", encoding="utf-8") as file:
                for line in file:
                    word = Word.parse(line)
                    if word is not None:
                        words.append(word)
        return words

    def load_stat(self, path: str) -> DictStats | None:
        if os.path.isdir(path):
            return None

        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        raw_stats = re.findall(r"- _(.*?)\n", content, flags=re.DOTALL | re.IGNORECASE)
        stats = [stat.split(" ")[-1] for stat in raw_stats]
        if len(stats) < 4:
            return None
        return DictStats(
            repetitions=int(stats[0]),
            average_comp=float(stats[1]),
            forgotten=int(stats[2]),
            known=int(stats[3]),
        )

    def save(
        self, path: str, words: list[Word], dict_stat: DictStats | None = None
    ) -> None:
        if os.path.isdir(path):
            return None

        with open(path, "w", encoding="utf-8") as file:
            if dict_stat is not None:
                file.writelines(render_dict_stat(dict_stat))
            for word in words:
                file.write(word.render() + "\n")

    @staticmethod
    def _list_files(path: str) -> list[str]:
        if os.path.isdir(path):
            return [os.path.join(path, f) for f in os.listdir(path)]
        return [path]
