from english_learning_app.ports.dict_repository import DictRepository
from english_learning_app.ports.terminal import Terminal
from english_learning_app.domain.word import Word
from english_learning_app.cli.display import (
    print_add_words_result,
    print_green,
    print_yellow,
)
from dataclasses import replace


def add_words(dict_repo: DictRepository, terminal: Terminal, path: str) -> None:
    words = dict_repo.load(path)
    dict_stat = dict_repo.load_stat(path)
    next_number = max([word.number for word in words], default=0) + 1
    words_counter = 0
    while True:
        english = terminal.read_line("Word: ").strip()
        if english == "q":
            print_yellow("exit")
            break
        russian = terminal.read_line("Translate: ").strip()
        word = Word(next_number, english, russian, 0, 0, False)
        words.append(word)
        print_green("added success")

        next_number += 1
        words_counter += 1

        dict_stat = replace(dict_stat, forgotten=dict_stat.forgotten + 1)

    dict_repo.save(path, words, dict_stat)

    print_add_words_result(words_counter)
