#!/usr/bin/python3

from english_learning_app.controllers.kernel import *
from english_learning_app.static.display import *
import traceback
import argparse
import re

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
        parser.add_argument(
            "--path_forgotten",
            type=str,
            help="Path to folder with English Forgotten words",
        )

        args = parser.parse_args()

        load_preview()

        if args.mode == 3:
            eng_dict = create_dict(args.path_forgotten)

            if len(eng_dict) <= 0:
                print("There are not Forgotten words")
                return

            cards = run_game(args.format, args.speed, eng_dict, args.path_forgotten, 2)

            graps.draw_graph(cards, args.path)

            delete_known_words(args.path_forgotten)

            return

        flag = int(
            input(
                "\nDo you wanna check the whole category or a separate list? (1 | 2) "
            ).strip()
        )

        dir_path = choose_category(args.path)

        filepath = dir_path if flag == 1 else choose_file(dir_path)

        if args.mode == 1:
            add_new_words(filepath)
        elif args.mode == 2:
            eng_dict = create_dict(filepath)
            # mode = choose_mode()
            # speed = choose_level()
            # if speed == -1:
            #     return
            cards = run_game(args.format, args.speed, eng_dict, filepath, flag)

            graps.draw_graph(cards, args.path)

    except Exception as e:
        print_red(f"Error: {traceback.format_exc()}")


def delete_known_words(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    result_lines = []

    pattern = r"\(🤯F\s*-\s*(\d+);\s*🧠U\s*-\s*(\d+)\)"
    for line in lines:
        match = re.search(pattern, line)
        if match and int(match.group(2)) - int(match.group(1)) < 2:
            result_lines.append(line)

    with open(filepath, "w", encoding="utf-8") as file:
        file.writelines(result_lines)


if __name__ == "__main__":
    main()
