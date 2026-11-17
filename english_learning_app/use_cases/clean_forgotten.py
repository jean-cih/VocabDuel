from english_learning_app.domain.dict_statistic import DictStats
from english_learning_app.domain.rules import is_mastered
from english_learning_app.ports.dict_repository import DictRepository
from english_learning_app.domain.word import Word
from dataclasses import replace


def clean_forgotten(dict_repo: DictRepository, path: str) -> int:
    words = dict_repo.load(path)

    kept: list[Word] = []
    index = 1
    for word in words:
        if not is_mastered(word):
            new = replace(word, number=index)
            kept.append(new)
            index += 1

    dict_repo.save(path, kept)
    return len(words) - len(kept)
