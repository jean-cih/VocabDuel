#!/usr/bin/python3

import re
from typing import Dict
import random
import time
import os

# Можно добавить игру с использованием слов в предложениии по уровню сложности, одно слово, два слова и т д

def load_game() -> int:

    print("\n === The English Game ===\n")
    time.sleep(1)
    greeting(" Hey, I'm Medora :)\n", " I'm a simple console trainer for memorizing words !!!")
    time.sleep(2)
    print("I have three options:")
    print(" 1. Adding new words")
    print(" 2. Training")
    print(" 3. Statistics output")
    time.sleep(1)

    try:
        while True:
            option = int(input(" Tap what you want to do: ").strip())
            if option not in [1, 2, 3]:
                print_yellow("Please, tap option from the ragne 1, 2, 3")
                continue
            return option
    except:
        raise ValueError("Unknown option for This Game")


def greeting(greet_text: str, discription: str):
    for char in greet_text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    
    time.sleep(1)

    for char in discription:
        print(char, end='', flush=True)
        time.sleep(0.05)

    time.sleep(1)

    for _ in range(9):
        print('\b' + ' ' + '\b', end='', flush=True)
        time.sleep(0.1)

    for char in "English words !!!\n":
        print(char, end='', flush=True)
        time.sleep(0.05)

    time.sleep(1)
    
    #print(" Obviously :)")

    for char in " Obviously ":
        print(char, end='', flush=True)
        time.sleep(0.05)
    time.sleep(1)
    print(":)")

    time.sleep(10)
    exit(1)
        

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


def create_dict(file_path: str) -> Dict:
    eng_dict = dict()
    with open(file_path, 'r') as file:
        for line in file:
            match_eng_word = re.search(r'\*\*(.+?)\*\*', line)
            match_trans = re.search(r' - (.*)', line)
            
            if match_eng_word and match_trans:
                eng_dict[match_eng_word.group(1)] = match_trans.group(1)

    return eng_dict        


def choose_mode() -> int:
    print("Format's Translate:")
    print("1.   Eng -> Rus")
    print("2.   Rus -> Eng")

    while True:
        try:
            mode = int(input("Choose The Game Mode: ").strip())

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

    print("\nThere is 6 Modes:")
    print(" 1.  Controlled")
    print(" 2.  Easy")
    print(" 3.  Medium")
    print(" 4.  Hard")
    print(" 5.  English God")
    print(" 6.  Exit")

    while True:
        try:
            level = int(input("Choose The Game Level: ").strip())

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
    while True:
        index = random.randint(0, len(eng_dict) - 1)
        if index in used:
            continue
        used.add(index)

        word = list(eng_dict.keys())[index]
        translate = eng_dict[word]
      
        if mode == 2:
            word, translate = translate, word
        
        print(f"\n[{index + 1}] Word: ", word, end="")
        time.sleep(speed) 
        if speed == 0.0:
            symbol = input().strip()
            if symbol == '':
                mark_known(filepath, index + 1, True)
                result += 1
            elif symbol == 'q':
                print(" == Exit ==")
                exit(1)
            else:
                mark_known(filepath, index + 1, False)

        print("Translate: ", translate)
        time.sleep(1.0)

        if len(used) == len(eng_dict):
            print("\n == Game Over ==")
            print(f"Result: {result * 100 //len(used)}% (result out of len(used))")
            break

        if len(used) % 10 == 0:
            print(f" == {len(used) * 100 // len(eng_dict)}% completed ==\n")


def mark_known(filepath: str, number: int, known: bool):
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
            index_file = int(input(" Choose The File's Number: ").strip())
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

    print("\n - Tap q to exit this mode -")

    while True:
        with open(filepath, "a") as file:
            new_word = input("\n WORD: ").strip().encode('utf-8', 'ignore').decode('utf-8')
            new_translate = input(" TRANSLATE: ").strip().encode('utf-8', 'ignore').decode('utf-8')

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
