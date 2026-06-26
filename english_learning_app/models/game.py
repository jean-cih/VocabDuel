#!/usr/bin/python3

from english_learning_app.controllers.kernel import *
from english_learning_app.static.display import *
import traceback

# Можно добавить игру с использованием слов в предложениии по уровню сложности, одно слово, два слова и т д
# а лучше перед этим предлогать из каких папок можно будет брать слова, можно из разных тем одновременно
# Также будет хорошо если реализую проверку корректности этих предложений посредством обращения к API-Deepseek

# Сделать среднее время запоминания, можно просто суммировать то время где я вспомнил и разделить на result


def main():
    path = "../../../mnt/c/Работа/MyBrainObsidian/personal-obsidian-vault/English/Dictionaries"

    try:
        stat = load_game()

        if stat == 3:
            statistics_output(path)
            return

        filepath = choose_file(path)

        if stat == 1:
            add_new_words(filepath)
        elif stat == 2:
            eng_dict = create_dict(filepath)
            mode = choose_mode()
            speed = choose_level()
            if speed == -1:
                return
            run_game(mode, speed, eng_dict, filepath)

    except Exception as e:
        print_red(f"Error: {traceback.format_exc()}")


if __name__ == "__main__":
    main()
