#!/usr/bin/python3

from english_learning_app.controllers.kernel import *
from english_learning_app.static.display import *
import traceback
import argparse

from english_learning_app.graphs import graps

# Можно добавить игру с использованием слов в предложениии по уровню сложности, одно слово, два слова и т д
# а лучше перед этим предлогать из каких папок можно будет брать слова, можно из разных тем одновременно
# Также будет хорошо если реализую проверку корректности этих предложений посредством обращения к API-Deepseek

# Сделать среднее время запоминания, можно просто суммировать то время где я вспомнил и разделить на result


def main():
    try:
        # reset_progress(path)

        parser = argparse.ArgumentParser(description="Game Parameters")

        parser.add_argument("--mode", type=int, default=2, help="Game Mode")
        parser.add_argument("--format", type=int, default=2, help="Translation format")
        parser.add_argument("--speed", type=int, default=1, help="Game speed")
        parser.add_argument(
            "--path", type=str, help="Path to folder with English dicts"
        )

        args = parser.parse_args()

        load_preview()

        filepath = choose_file(args.path)

        if args.mode == 1:
            add_new_words(filepath)
        elif args.mode == 2:
            eng_dict = create_dict(filepath)
            # mode = choose_mode()
            # speed = choose_level()
            # if speed == -1:
            #     return
            cards = run_game(args.format, args.speed, eng_dict, filepath)

            graps.draw_graph(cards, args.path)

    except Exception as e:
        print_red(f"Error: {traceback.format_exc()}")


if __name__ == "__main__":
    main()
