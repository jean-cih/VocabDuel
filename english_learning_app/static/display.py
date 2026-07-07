import time
import os


def load_preview():

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


def typing(text: str, delay: float):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)


def typing_delete(bound: int, delay: float):
    for _ in range(bound):
        print("\b" + " " + "\b", end="", flush=True)
        time.sleep(delay)


def greeting(greet_text: str, discription: str):
    typing(greet_text, 0.05)
    time.sleep(1)

    typing(discription, 0.05)
    time.sleep(1)

    typing_delete(9, 0.1)

    typing("English words !!!\n", 0.05)
    time.sleep(1)

    typing(" Obviously :)\n", 0.05)
    time.sleep(1)


def choose_option(text: str):
    typing(text, 0)
    print(" 1. Top-up")
    print(" 2. Practice")


def print_green(text: str):
    print(f"\033[32m -- {text} --\033[0m")


def print_red(text: str):
    print(f"\033[31m -- {text} --\033[0m")


def print_yellow(text: str):
    print(f"\033[33m -- {text} --\033[0m")


def print_blue(text: str):
    print(f"\033[34m -- {text} --\033[0m")
