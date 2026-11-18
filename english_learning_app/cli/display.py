import time
import sys

_COLORS = {
    "green": "\033[32m",
    "red": "\033[31m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "purple": "\033[35m",
    "reset": "\033[0m",
}

_USE_COLOR = True


def set_color(enabled: bool) -> None:
    global _USE_COLOR
    _USE_COLOR = enabled


def _c(text: str, color: str) -> str:
    return f"{_COLORS[color]}{text}{_COLORS['reset']}" if _USE_COLOR else text


def load_preview(description_mode: str) -> bool:
    print("\n === The English Game ===\n")

    answer = input("Do you wanna understand in detail? (Yes | No) ").strip().lower()
    if answer == "yes":
        time.sleep(0.5)
        greeting(
            "\n Good\n I'm Medora :)\n",
            " I'm a simple console trainer for memorizing words !!!",
        )
        time.sleep(2)

        typing(f"\n You chose '{description_mode}'\n\n", 0.05)
        time.sleep(1)
        return False
    return True


def typing(text: str, delay: float) -> None:
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)


def typing_delete(bound: int, delay: float) -> None:
    for _ in range(bound):
        print("\b" + " " + "\b", end="", flush=True)
        time.sleep(delay)


def greeting(greet_text: str, discription: str) -> None:
    typing(greet_text, 0.05)
    time.sleep(1)

    typing(discription, 0.05)
    time.sleep(1)

    typing_delete(9, 0.1)

    typing("English words !!!\n", 0.05)
    time.sleep(1)

    typing(" Obviously :)\n", 0.05)
    time.sleep(1)


def choose_option(text: str) -> None:
    typing(text, 0)
    print(" 1. Top-up")
    print(" 2. Practice")


def print_green(text: str, start: str = "", sep: str = "\n") -> None:
    color_text = _c(text, "green")
    print(f"{start}{color_text}{sep}")


def print_red(text: str, sep: str = "\n") -> None:
    color_text = _c(text, "red")
    print(f"{color_text}{sep}")


def print_yellow(text: str, start: str = "\n", sep: str = "\n") -> None:
    color_text = _c(text, "yellow")
    print(f"{start}{color_text}{sep}")


def print_blue(text: str, sep: str = "\n") -> None:
    color_text = _c(text, "blue")
    print(f"{color_text}{sep}")


def print_purple(text: str, start: str = "", sep: str = "\n") -> None:
    color_text = _c(text, "purple")
    print(f"{start}{color_text}{sep}")


def print_add_words_result(words_counter: int) -> None:
    print_green(f"- Added Words: {words_counter} -")


def print_session_result(success_words: int, all_words: int, cards: int) -> None:
    percent_full_list: int = int(100 * success_words / all_words)
    percent_comp: int = int(100 * success_words / cards)
    print_purple(
        f"- Result: {success_words}/{all_words} ({percent_full_list}%) | Comprehension: ({percent_comp}%) -"
    )


def print_interim_result(percent: float) -> None:
    print_green(f"- Completed by {percent:.1f}% -")


def hide_cursor() -> None:
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor() -> None:
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def highlight(text: str, bg: tuple[int, int, int], fg: int = 30) -> str:
    if not _USE_COLOR:
        return text
    r, g, b = bg
    return f"\033[48;2;{r};{g};{b}m\033[{fg}m {text} \033[0m"


def print_word_prompt(number: int, text: str) -> None:
    print(f"Word {number}: {highlight(text, (255, 165, 0), 30)}")


def print_translate_prompt(text: str) -> None:
    print(f"Translate: {highlight(text, (128, 0, 128), 97)}")
