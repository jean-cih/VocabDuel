import random

from english_learning_app.ports.dict_repository import DictRepository
from english_learning_app.ports.terminal import Terminal
from english_learning_app.domain.rules import apply_answer


def play_session(
    dict_repo: DictRepository, terminal: Terminal, timeout: float, path: str
) -> tuple[int, int, int, str, int]:
    words = dict_repo.load(path)
    dict_stat = dict_repo.load_stat(path)

    indices = [i for i in range(len(words))]
    random.shuffle(indices)

    known = unknown = 0
    cards = 0
    for index in indices:
        answer = terminal.read_line(f"Word: {words[index].english}\t")
        terminal.wait_key(timeout)
        if answer == "q":
            break

        terminal.read_line(f"Translate: {words[index].russian}\t")
        remembered = answer == ""
        if remembered and not words[index].known:
            known += 1
        elif not remembered and words[index].known:
            unknown += 1
        words[index] = apply_answer(words[index], remembered)

        cards += 1

    if cards > 0:
        dict_stat = dict_stat.add_session(cards, unknown, known)

    dict_repo.save(path, words, dict_stat)

    topic = path.split("/")[-2]

    return cards, known, unknown, topic, len(words)
