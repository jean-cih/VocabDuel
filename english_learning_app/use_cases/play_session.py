import random

from english_learning_app.ports.dict_repository import DictRepository
from english_learning_app.ports.terminal import Terminal
from english_learning_app.domain.rules import apply_answer
from english_learning_app.cli import display
from english_learning_app.domain.word import Word
from dataclasses import replace

MAX_PERCENT = 100.0


def play_session(
    dict_repo: DictRepository,
    terminal: Terminal,
    timeout: float | None,
    path: str,
    format_session: int,
) -> tuple[int, int, int, str, int, list[Word]]:
    words = dict_repo.load(path)
    dict_stat = dict_repo.load_stat(path)

    indices = [i for i in range(len(words))]
    random.shuffle(indices)

    display.print_purple(f"All Words: {len(indices)}", "\n", "")
    display.print_red(f"{timeout} sec to answer", "\n")

    input("Tap Enter to start session\n").strip()

    forgotten_words: list[Word] = []
    known = unknown = success_words = 0
    cards = 0
    for index in indices:
        front_side: str = words[index].english
        other_side: str = words[index].russian

        if format_session == 2:
            front_side, other_side = other_side, front_side

        display.print_word_prompt(words[index].number, front_side)
        # not_exit = terminal.wait_key_blinking("  Tap any key to reveal…", timeout, 0.5)
        print("  Tap Enter to reveal…\t")
        terminal.wait_key(timeout)

        display.print_translate_prompt(other_side)
        # answer = terminal.wait_key_blinking("  [Enter] know   [any] don't   [q] quit", timeout, 0.5)
        answer = input("  [Enter] know   [any] don't   [q] quit\t").strip()

        if answer == "q":
            display.print_yellow(" - exit -")
            break

        remembered = answer == ""
        if remembered and words[index].known:
            success_words += 1
            display.print_green(" - 🔥 already done -")
        elif remembered and not words[index].known:
            known += 1
            display.print_green(" - 👍 done -")
        elif not remembered and words[index].known:
            unknown += 1
            display.print_blue(" - 🤷 forgot -")
            forgotten_words.append(words[index])
        elif not remembered and not words[index].known:
            display.print_blue(" - 🙃 unknown -")
            forgotten_words.append(words[index])

        words[index] = apply_answer(words[index], remembered)

        cards += 1
        if cards % (compute_divider(len(indices)) * len(indices) / 100) == 0:
            percent: float = MAX_PERCENT * cards / len(indices)
            display.print_interim_result(percent)

    if cards > 0 and dict_stat is not None:
        dict_stat = dict_stat.add_session(cards, unknown, known)

    dict_repo.save(path, words, dict_stat)

    success_words += known
    display.print_session_result(success_words, len(words), cards)

    topic = path.split("/")[-2]

    return cards, known, unknown, topic, len(words), forgotten_words


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


def write_forgotten_word(
    dict_repo: DictRepository, new_words: list[Word], path: str
) -> None:
    words_in_file = dict_repo.load(path)
    next_number = max([word.number for word in words_in_file], default=0) + 1

    for word in new_words:
        words_in_file.append(replace(word, number=next_number, u=0, f=0, known=False))
        next_number += 1

    dict_repo.save(path, words_in_file)
