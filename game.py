#!/usr/bin/python3

import re
from typing import Dict
import random
import time
import os


# Можно добавить вывод статистики

# Можно добавить возможность пополнеиня словаря

# Добавить в игру отмечание выученных слов

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
    print("Modes:")
    print("1 - (to eng from rus)")
    print("2 - (to rus from eng)")

    while True:
        try:
            mode = int(input("Choose The Game Mode: ").strip())

            if mode not in [1, 2]:
                print("Please, enter the number 1 or 2")
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
            5: 0.5
    }

    print("\nThere is 3 Levels")
    print(" 1 - controlled")
    print(" 2 - easy")
    print(" 3 - medium")
    print(" 4 - hard")
    print(" 5 - english God")

    while True:
        try:
            level = int(input("Choose The Game Level: ").strip())

            if level not in list(range(1, 6)):
                print("Please, enter the number 1, 2, 3, 4 or 5")
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
        
        print(f"\n[{index + 1}] Word: ", word)
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
    else:
        new_content = content.replace(f"{number}. 🔥**", f"{number}. **")

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
                print(f"Please, enter the number from the range {list(range(1, num))}")
                continue
            return paths[index_file - 1]
    except:
        raise ValueError("Unknown file's number")


if __name__ == "__main__":
    
    print(" === The English Game ===\n")

    try:
        path = "../../../../mnt/c/Users/user/Job/Smth/Backend/English/Dictionaries"

        filepath = choose_file(path)

        eng_dict = create_dict(filepath)

        mode = choose_mode()
        speed = choose_level()
        run_game(mode, speed, eng_dict, filepath)
    except Exception as e:
        print(f"Error: {e}")
