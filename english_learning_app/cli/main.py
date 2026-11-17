#!/usr/bin/python3
import argparse
from datetime import date

from english_learning_app.cli.display import print_green
from english_learning_app.infra.markdown_dict_repo import MarkdownDictRepository
from english_learning_app.infra.markdown_stats_repo import MarkdownStatsRepository
from english_learning_app.infra.posix_terminal import PosixTerminal
from english_learning_app.use_cases.play_session import play_session
from english_learning_app.use_cases.clean_forgotten import clean_forgotten
from english_learning_app.use_cases.update_statistics import update_statistics
from english_learning_app.use_cases.add_words import add_words
from english_learning_app.cli import menus, display


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Game Parameters")

    parser.add_argument("--mode", type=int, default=2, help="Game Mode")
    parser.add_argument("--format", type=int, default=2, help="Translation format")
    parser.add_argument("--speed", type=int, default=1, help="Game speed")
    parser.add_argument("--path", type=str, help="Path to folder with English dicts")
    parser.add_argument(
        "--path_forgotten",
        type=str,
        help="Path to file with English Forgotten words",
    )
    parser.add_argument(
        "--path_stats",
        type=str,
        help="Path to statistics file",
    )
    return parser


def create_path_to_dict(path: str, mode: int) -> str:
    dir_path = menus.choose_category(path)
    filepath = menus.choose_file(dir_path) if mode != 4 else dir_path
    return filepath


def main() -> None:
    try:
        args = build_parser().parse_args()

        dict_repo = MarkdownDictRepository()
        stats_repo = MarkdownStatsRepository()
        terminal = PosixTerminal()

        with terminal.hidden_cursor():
            desc_mode = menus.choose_mode(args.mode)
            if display.load_preview(desc_mode):
                print_green(f"| -- {desc_mode} -- |", "\n")

            cards = unknown = known = max_words = 0
            topic = ""
            if args.mode == 1:
                filepath = create_path_to_dict(args.path, args.mode)
                add_words(dict_repo, terminal, filepath)
            elif args.mode == 2:
                filepath = create_path_to_dict(args.path, args.mode)
                format_session = menus.choose_format()
                cards, known, unknown, topic, max_words = play_session(
                    dict_repo, terminal, args.speed, filepath, format_session
                )
            elif args.mode == 3:
                format_session = menus.choose_format()
                cards, _, _, _, _ = play_session(
                    dict_repo, terminal, args.speed, args.path_forgotten, format_session
                )
                clean_forgotten(dict_repo, args.path_forgotten)
            elif args.mode == 4:
                format_session = menus.choose_format()
                filepath = create_path_to_dict(args.path, args.mode)
                cards, _, _, _, _ = play_session(
                    dict_repo, terminal, args.speed, filepath, format_session
                )
            else:
                raise NotImplementedError("Unsupported option")

        update_statistics(
            stats_repo, args.path_stats, cards, unknown, known, topic, max_words
        )

    except Exception as e:
        display.print_red(f"Error: {e}")


if __name__ == "__main__":
    main()
