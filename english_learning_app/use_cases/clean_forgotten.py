from english_learning_app.domain.rules import is_mastered
from english_learning_app.ports.dict_repository import DictRepository


def clean_forgotten(dict_repo: DictRepository, path: str) -> int:
    words = dict_repo.load(path)
    kept = [w for w in words if is_mastered(w)]
    dict_repo.save(path, kept)
    return len(words) - len(kept)
