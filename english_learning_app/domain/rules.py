from english_learning_app.domain.word import Word
from dataclasses import replace


def is_mastered(word: Word, threshold: int = 2) -> bool:
    return word.u - word.f >= threshold


def apply_answer(word: Word, remember: bool) -> Word:
    if remember:
        return replace(word, u=word.u + 1, known=True)
    else:
        return replace(word, f=word.f + 1, known=False)
