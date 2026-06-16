import time
import os


def load_game() -> int:

    print("\n === The English Game ===\n")

    answer = input("Do you wanna understand in detail? (Yes | No) ").strip().lower()
    if answer == "yes":
        time.sleep(0.5)
        greeting("\n Good\n I'm Medora :)\n", " I'm a simple console trainer for memorizing words !!!")
        time.sleep(2)

    choose_option("\n I can offer you something:\n")
    
    try:
        while True:
            option = int(input(" What do You want: ").strip())
            if option not in [1, 2, 3]:
                print_yellow("Please, tap option from the ragne 1, 2, 3")
                continue
            return option
    except:
        raise ValueError("Unknown option for This Game")

def typing(text: str, delay: float):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def typing_delete(bound: int, delay: float):
    for _ in range(bound):
        print('\b' + ' ' + '\b', end='', flush=True)
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
    print(" 3. Progress")


def statistics_output(folder_path: str) -> None:
    print("\n\n == Statistics ==\n")

    paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            paths.append(os.path.join(root, file))

    # Нет защиты от уникальных слов
    all_known_words = 0
    all_unknown_words = 0
    for path in paths:
        with open(path, "r") as file:
            for line in file:
                index_spot = line.find(".")
                if index_spot == -1:
                    continue
                index = line.find("🔥")
                if index >= 0:
                    all_known_words += 1
                else:
                    all_unknown_words += 1

    print(f"All known words: {all_known_words}")
    print(f"All unknown words: {all_unknown_words}")
    print(f"Total words: {all_known_words + all_unknown_words}\n")

def print_green(text: str):
    print(f"\033[32m -- {text} --\033[0m")

def print_red(text: str):
    print(f"\033[31m -- {text} --\033[0m")

def print_yellow(text: str):
    print(f"\033[33m -- {text} --\033[0m")

def print_blue(text: str):
    print(f"\033[34m -- {text} --\033[0m")
