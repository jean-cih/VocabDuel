from typing import Dict, Set
import re
import sys
import tty
import time
import termios
import random
import select
import os

from english_learning_app.static.display import *


def create_dict(file_path: str) -> Dict[str, tuple[str, int]]:
    option = int(
        input("Do you wanna learn all or only unknown words? (1 | 2) ").strip()
    )

    eng_dict = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:

            if option == 2 and "🔥" in line:
                continue

            index = line.find(".")
            if index == -1:
                continue

            try:
                number = int(line[:index].strip())
            except ValueError:
                continue

            pattern = r"\*\*([^*]+)\*\*\s*[\-–—]\s*([^_]+?)(?:\s*(_)|$)"

            match = re.search(pattern, line)
            if match:
                english = match.group(1)
                russian = match.group(2).strip()
                bracket_part = match.group(3)

                if bracket_part:
                    bracket_match = re.search(r"_.*$", line)
                    bracket_full = bracket_match.group(0) if bracket_match else ""

                    numbers = bracket_full.split(";")
                    f_index = numbers[0].find("- ") + 2

                    u_index = numbers[1].find("- ") + 2
                    u_end_index = numbers[1].find(")_")

                    eng_dict[english] = (
                        russian,
                        number,
                        int(numbers[0][f_index:]),
                        int(numbers[1][u_index:u_end_index]),
                    )
                else:
                    eng_dict[english] = (russian, number, 0, 0)

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
    levels = {1: 0.0, 2: 4.0, 3: 2.0, 4: 1.0, 5: 0.5, 6: -1}

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
        result = run_time_game(mode, speed, eng_dict, used, filepath)
    else:
        result = run_control_game(mode, eng_dict, used, filepath)

    print("\n == Game Over ==")
    print(f"Result: {result * 100 //len(eng_dict)}% ({result} out of {len(eng_dict)})")

    game_over_write(filepath, result)


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
                if ch != "q":
                    return True
                elif ch == "q":
                    return False
        return None

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def run_time_game(
    mode: int, speed: float, created_dict: Dict, used: Set, filepath: str
) -> int:
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

        print(f"\n[{created_dict[word][1]}] - Word: ", word.strip(), end=" ")

        result_tap = wait_for_non_q(speed)
        if result_tap is True:
            mark_known(filepath, created_dict[word][1] + 1, True)
            result += 1
        elif result_tap is False:
            break
        else:
            mark_known(filepath, created_dict[word][1], False)

        print("Translate: ", translate.strip(), end=" ")

        if len(used) % 10 == 0:
            print(f" == {len(used) * 100 // len(created_dict)}% completed ==\n")

        if len(used) == len(created_dict):
            break

        time.sleep(1.0)

    return result


def run_control_game(mode: int, created_dict: Dict, used: Set, filepath: str) -> int:
    result = 0
    while True:
        index = random.randint(0, len(created_dict) - 1)
        if index in used:
            continue

        used.add(index)

        word = list(created_dict.keys())[index]
        translate = created_dict[word][0]
        number = created_dict[word][1]
        forgettable = created_dict[word][2]
        understandable = created_dict[word][3]

        if mode == 2:
            word, translate = translate, word

        print(f"\n[{number}] Word: ", word.strip(), end=" ")
        input()
        print("Translate: ", translate.strip(), end=" ")
        symbol = input().strip()
        if symbol == "":
            mark_known(filepath, number, forgettable, understandable, True)
            result += 1
        elif symbol == "q":
            break
        else:
            mark_known(filepath, number, forgettable, understandable, False)

        if len(used) % 10 == 0:
            print(f" == {len(used) * 100 // len(created_dict)}% completed ==\n")

        if len(used) == len(created_dict):
            break

        time.sleep(1.0)

    return result


def mark_known(filepath: str, number: int, f_count: int, u_count: int, known: bool):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.readlines()

    new_lines = []
    found = False

    for line in lines:
        if line.strip().startswith(f"{number}."):
            found = True

            stat_index = line.find("_(")
            if stat_index == -1:
                line = line[:-1] + " _(🤯F - 0; 🧠U - 0)_\n"

            if known:
                line_with_stat = line.replace(
                    f"_(🤯F - {f_count}; 🧠U - {u_count})_",
                    f"_(🤯F - {f_count}; 🧠U - {u_count + 1})_",
                )
                if "🔥" not in line:
                    new_line = line_with_stat.replace(
                        f"{number}. **", f"{number}. 🔥**"
                    )
                    print_green("studied")
                else:
                    new_line = line_with_stat
                    print_green("already studied")
            else:
                line_with_stat = line.replace(
                    f"_(🤯F - {f_count}; 🧠U - {u_count})_",
                    f"_(🤯F - {f_count + 1}; 🧠U - {u_count})_",
                )
                new_line = line_with_stat.replace(f"{number}. 🔥**", f"{number}. **")
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
                print_yellow(
                    f"Please, enter the number from the range {list(range(1, num))}"
                )
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
            new_word = (
                input("\n Word: ").strip().encode("utf-8", "ignore").decode("utf-8")
            )
            new_translate = (
                input(" Translate: ").strip().encode("utf-8", "ignore").decode("utf-8")
            )

            if new_word == "q" or new_translate == "q":
                file.write("---\n")
                break

            file.write(f"{number_new_word}. **{new_word}** - {new_translate}\n")
            print_green(f"{new_word} was added")
            number_new_word += 1


def game_over_write(filepath: str, round_result: int):
    template = {
        "The Number of page repetitions": 0,
        "Average page comprehension (%)": 0.0,
        "The Number of 🤯 Forgettable words": 0,
        "The Number of 🧠 Understandable words": 0,
    }

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    understandable_words_count = content.count("🔥")
    all_words = content.count("**") // 2 - 1

    stat_pattern = r"\*\*Statistic:\*\*.*?(?=\n\n|\Z|(?=\n\d+\.))"
    stat_match = re.search(stat_pattern, content, re.DOTALL)

    if stat_match:
        stat_block = stat_match.group(0)
        for key in template.keys():
            pattern = rf"{re.escape(key)}:\s*([0-9]+)"
            match = re.search(pattern, stat_block)
            if match:
                template[key] = int(match.group(1))

        template["The Number of page repetitions"] += 1

        content = content.replace(stat_block, "")
    else:
        template["The Number of page repetitions"] = 1

    template["Average page comprehension (%)"] = round(
        understandable_words_count * 100 / all_words, 1
    )
    template["The Number of 🤯 Forgettable words"] = (
        all_words - understandable_words_count
    )
    template["The Number of 🧠 Understandable words"] = understandable_words_count

    new_stat_block = "**Statistic:**\n"
    for key, value in template.items():
        new_stat_block += f"- _{key}: {value}\n"
    new_stat_block += "\n"

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(new_stat_block)
        file.write(content.lstrip())
