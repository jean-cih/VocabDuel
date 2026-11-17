import random

from english_learning_app.ports.dict_repository import DictRepository
from english_learning_app.ports.terminal import Terminal
from english_learning_app.domain.rules import apply_answer
from english_learning_app.cli.display import (
    print_green,
    print_blue,
    print_yellow,
    print_interim_result,
    print_session_result,
    print_purple,
)

MAX_PERCENT = 100.0


def play_session(
    dict_repo: DictRepository, terminal: Terminal, timeout: float, path: str
) -> tuple[int, int, int, str, int]:
    words = dict_repo.load(path)
    dict_stat = dict_repo.load_stat(path)

    indices = [i for i in range(len(words))]
    random.shuffle(indices)

    print_purple(f"All Words: {len(indices)}", "\n")

    known = unknown = success_words = 0
    cards = 0
    for index in indices:
        not_exit = terminal.read_line(
            f"Word {words[index].number}: \033[48;2;255;165;0m\033[30m {words[index].english} \033[0m\nTap ... "
        )
        terminal.wait_key(timeout)
        if not_exit == "q":
            print_yellow("exit")
            break

        answer = terminal.read_line(
            f"Translate: \033[48;2;128;0;128m\033[97m {words[index].russian} \033[0m\nCheck (+ -) "
        )

        remembered = answer == "" or answer == "+"
        if remembered and words[index].known:
            success_words += 1
            print_green("already done")
        elif remembered and not words[index].known:
            known += 1
            print_green("done")
        elif not remembered and words[index].known:
            unknown += 1
            print_blue("forgot")
        elif not remembered and not words[index].known:
            print_blue("unknown")

        words[index] = apply_answer(words[index], remembered)

        cards += 1
        if cards % (compute_divider(len(indices)) * len(indices) / 100) == 0:
            percent: float = MAX_PERCENT * cards / len(indices)
            print_interim_result(percent)

    if cards > 0 and dict_stat is not None:
        dict_stat = dict_stat.add_session(cards, unknown, known)

    dict_repo.save(path, words, dict_stat)

    success_words += known
    print_session_result(success_words, len(words), cards)

    topic = path.split("/")[-2]

    return cards, known, unknown, topic, len(words)


def compute_divider(all_words: int) -> int:
    dict_dividers: dict[int, int] = {
        1000: 2,
        100: 10,
        10: 20,
    }
    for key in dict_dividers.keys():
        if len(str(key)) == len(str(all_words)):
            return dict_dividers[key]
    return 1
