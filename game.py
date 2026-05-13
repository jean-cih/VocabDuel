#!/usr/bin/python3

import re
from typing import Dict, Set
import random
import time
import os
import sys
import select
import termios
import tty

# Можно добавить игру с использованием слов в предложениии по уровню сложности, одно слово, два слова и т д

# Сделать среднее время запоминания, можно просто суммировать то время где я вспомнил и разделить на result

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


def create_dict(file_path: str) -> Dict[str, tuple[str, int]]:
    option = int(input("Do you wanna learn all or only unknown words? (1 | 2) ").strip())

    eng_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
    
            if option == 2 and "🔥" in line:
                continue

            match_eng_word = re.search(r'\*\*(.+?)\*\*', line)
            match_trans = re.search(r'[\-–—]\s*(.*)$', line)

            if not match_eng_word or not match_trans:
                continue

            index = line.find('.')
            if index == -1:
                continue

            try:
                number = int(line[:index].strip())
            except ValueError:
                continue

            eng_word = match_eng_word.group(1).strip()
            translation = match_trans.group(1).strip()

            eng_dict[eng_word] = (translation, number)

    return eng_dict


def choose_mode() -> int:
    print("\n == Options ==\n")
    print("1.   Eng -> Rus")
    print("2.   Rus -> Eng")

    while True:
        try:
            mode = int(input("Choose Opt: ").strip())

            if mode not in [1, 2]:
                print_yellow("Please, enter the number 1 or 2")
                continue
            return mode
        except:
            raise ValueError("Unknown mode for Game")


def choose_level() -> float:
    levels = {
            1: 0.0,
            2: 4.0,
            3: 2.0,
            4: 1.0,
            5: 0.5,
            6: -1
    }

    print("\n == All Modes ==\n")
    print(" 1.  Controlled")
    print(" 2.  Easy")
    print(" 3.  Medium")
    print(" 4.  Hard")
    print(" 5.  English God")
    print(" 6.  Exit")

    while True:
        try:
            level = int(input("Choose Mode: ").strip())

            if level not in list(range(1, 7)):
                print_yellow("Please, enter the number 1, 2, 3, 4, 5 or 6")
                continue
            return levels[level]
        except:
            raise ValueError("Unknown level for Game")


def run_game(mode: int, speed: float, eng_dict: Dict, filepath: str) -> None:

    print("\nStart The Process")
    print(20 * "-")

    used = set()
    result = 0
    if speed > 0:
        result = run_time_game(speed, eng_dict, used)
    else:
        result = run_control_game(eng_dict, used)

    print("\n == Game Over ==")
    print(f"Result: {result * 100 //len(eng_dict)}% ({result} out of {len(eng_dict)})")


def wait_for_non_q(speed: float):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        tty.setraw(fd)
        
        start_time = time.time()
        last_printed_second = -1
        while time.time() - start_time <= speed + 1:
            current_second = speed - (time.time() - start_time) + 1

            print(f"\r[{current_second:.1f} s]", end=" ", flush=True)
            last_printed_second = current_second

            if select.select([sys.stdin], [], [], 0.05)[0]:
                ch = sys.stdin.read(1).lower()
                if ch != 'q':
                    return True
                elif ch == 'q':
                    return False
        return None
        
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def run_time_game(speed: float, created_dict: Dict, used: Set) -> int:
    result = 0

    while True:
        index = random.randint(0, len(created_dict) - 1)
        if index in used:
            continue

        used.add(index)

        word = list(created_dict.keys())[index]
        translate = created_dict[word][0]
      
        if mode == 2:
            word, translate = translate, word    

        print(f"\n[{created_dict[word][1]}] - Word: ", word.strip())

        result_tap = wait_for_non_q(speed)
        if result_tap is True:
            mark_known(filepath, created_dict[word][1]  + 1, True)
            result += 1
        elif result_tap is False:
            break
        else:
            mark_known(filepath, created_dict[word][1], False) 

        print("Translate: ", translate.strip())

        if len(used) % 10 == 0:
            print(f" == {len(used) * 100 // len(eng_dict)}% completed ==\n")

        if len(used) == len(created_dict):
            break

        time.sleep(1.0)

    return result


def run_control_game(created_dict: Dict, used: Set) -> int:
    result = 0

    while True:
        index = random.randint(0, len(created_dict) - 1)
        if index in used:
            continue

        used.add(index)

        word = list(created_dict.keys())[index]
        translate = created_dict[word][0]     
        number = created_dict[word][1]
     
        if mode == 2:
            word, translate = translate, word

        print(f"\n[{number}] Word: ", word.strip(), end=" ")
        input()
        print("Translate: ", translate.strip())
        symbol = input().strip()
        if symbol == '':
            mark_known(filepath, number, True)
            result += 1
        elif symbol == 'q':
            break
        else:
            mark_known(filepath, number, False)

        if len(used) % 10 == 0:
            print(f" == {len(used) * 100 // len(eng_dict)}% completed ==\n")

        if len(used) == len(created_dict):
            break

        time.sleep(1.0)

    return result


def mark_known1(filepath: str, number: int, known: bool):
    with open(filepath, "r") as file:
        content = file.read()

    if known:
        new_content = content.replace(f"{number}. **", f"{number}. 🔥**")
        print_green("studied")
    else:
        new_content = content.replace(f"{number}. 🔥**", f"{number}. **")
        print_blue("forgot")

    with open(filepath, "w") as file:
        file.write(new_content)


def mark_known(filepath: str, number: int, known: bool):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    new_lines = []
    found = False

    for line in lines:
        if line.strip().startswith(f"{number}."):
            found = True
            if known:
                if "🔥" not in line:
                    new_line = line.replace(f"{number}. **", f"{number}. 🔥**")
                    print_green("studied")
                else:
                    new_line = line
                    print_green("already studied")
            else:
                new_line = line.replace(f"{number}. 🔥**", f"{number}. **")
                print_blue("forgot")
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if not found:
        print(f"Word with number {number} not found!")

    with open(filepath, "w", encoding="utf-8") as file:
        file.writelines(new_lines)


def choose_file(folder_path: str) -> str:

    print("\n == All Awailable Dictionaries ==\n")

    paths = []
    num = 1
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            print(f"{num}. {file}")
            paths.append(os.path.join(root, file))
            num += 1

    try:
        while True:
            index_file = int(input(" Choose The File: ").strip())
            if index_file not in list(range(1, num)):
                print_yellow(f"Please, enter the number from the range {list(range(1, num))}")
                continue
            return paths[index_file - 1]
    except:
        raise ValueError("Unknown file's number")


def add_new_words(filepath: str):
    
    number_new_word = 1
    with open(filepath, "r") as file:
        for line in file:
            index_spot = line.find(".")

            if index_spot >= 0:
                number_new_word += 1

    print("\n - Tap q to exit -")

    while True:
        with open(filepath, "a") as file:
            new_word = input("\n Word: ").strip().encode('utf-8', 'ignore').decode('utf-8')
            new_translate = input(" Translate: ").strip().encode('utf-8', 'ignore').decode('utf-8')

            if new_word == 'q' or new_translate == 'q':
                file.write("---\n")
                break

            file.write(f"{number_new_word}. **{new_word}** - {new_translate}\n")
            print_green(f"{new_word} was added")
            number_new_word += 1
          








def print_green(text: str):
    print(f"\033[32m -- {text} --\033[0m")

def print_red(text: str):
    print(f"\033[31m -- {text} --\033[0m")

def print_yellow(text: str):
    print(f"\033[33m -- {text} --\033[0m")

def print_blue(text: str):
    print(f"\033[34m -- {text} --\033[0m")

if __name__ == "__main__":
    path = "../../../../mnt/c/Users/user/Job/Smth/Backend/English/Dictionaries"

    try:
        while True:
            stat = load_game()

            if stat == 3:
                statistics_output(path)
                break

            filepath = choose_file(path)

            if stat == 1:
                add_new_words(filepath)
            elif stat == 2:
                eng_dict = create_dict(filepath)
                mode = choose_mode()
                speed = choose_level()
                if speed == -1:
                    break
                run_game(mode, speed, eng_dict, filepath)

    except Exception as e:
        print_red(f"Error: {e}")
        
