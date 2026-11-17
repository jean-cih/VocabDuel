import time


def load_preview() -> None:

    print("\n === The English Game ===\n")

    answer = input("Do you wanna understand in detail? (Yes | No) ").strip().lower()
    if answer == "yes":
        time.sleep(0.5)
        greeting(
            "\n Good\n I'm Medora :)\n",
            " I'm a simple console trainer for memorizing words !!!",
        )
        time.sleep(2)

    # choose_option("\n I can offer you something:\n")
    #
    # try:
    #     while True:
    #         option = int(input(" What do You want: ").strip())
    #         if option not in [1, 2]:
    #             print_yellow("Please, tap option from the ragne 1, 2")
    #             continue
    #         return option
    # except:
    #     raise ValueError("Unknown option for This Game")


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


def print_green(text: str, sep: str = "\n") -> None:
    print(f"\033[32m -- {text} --\033[0m{sep}")


def print_red(text: str, sep: str = "\n") -> None:
    print(f"\033[31m -- {text} --\033[0m{sep}")


def print_yellow(text: str, sep: str = "\n") -> None:
    print(f"\033[33m -- {text} --\033[0m{sep}")


def print_blue(text: str, sep: str = "\n") -> None:
    print(f"\033[34m -- {text} --\033[0m{sep}")


def print_purple(text: str, start: str = "", sep: str = "\n") -> None:
    print(f"{start}\033[35m -- {text} --\033[0m{sep}")


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
