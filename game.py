import re
from typing import Dict
import random
import time


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
            mode = int(input("Choose The Game Mode: "))

            if mode not in [1, 2]:
                print("Please choose the number 1 or 2")
                continue
            return mode
        except:
            raise ValueError("Unknown mode for Game")


def choose_level() -> float:
    levels = {
            1: 0.5,
            2: 1.0,
            3: 2.0,
            4: 3.0
    }

    print("\nThere is 3 Levels")
    print(" 4 - easy")
    print(" 3 - medium")
    print(" 2 - hard")
    print(" 1 - english God")

    while True:
        try:
            level = int(input("Choose The Game Level: "))

            if level not in list(range(1, 5)):
                print("Please enter the number 1, 2, 3 or 4")
                continue
            return levels[level]
        except:
            raise ValueError("Unknown level for Game")


def run_game(mode: int, eng_dict: Dict) -> None:

    speed = choose_level()

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
        
        print(f"[{index + 1}] Word: ", word, sep=" ", end="")
        #time.sleep(speed)
        symbol = input()
        if symbol == '':
            result += 1
        print("Translate: ", translate, end="\n\n")
        #time.sleep(1)

        if len(used) == len(eng_dict):
            print("\n == Game Over ==")
            print(f"Result: {result * 100 //len(used)}% (result out of len(used))")
            break

        if len(used) % 10 == 0:
            print(f" == {len(used) * 100 // len(eng_dict)}% completed ==\n")


if __name__ == "__main__":

    print(" === The English Game ===\n")

    path = "../../../../mnt/c/Users/user/Job/Smth/Backend/English/Dictionaries/The-Curious-Incident-of-the-Dog-in-the-Night-Time.md"
    eng_dict = create_dict(path)

    mode = choose_mode()
    run_game(mode, eng_dict)
