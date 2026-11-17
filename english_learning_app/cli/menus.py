import os
from english_learning_app.cli.display import print_yellow


def choose_category(folder_path: str) -> str | None:
    print(" == All Available Categories ==\n")

    paths = []
    num = 1
    for root, dirs, files in os.walk(folder_path):
        for direct in dirs:
            dir_path = os.path.join(root, direct)
            if os.path.isdir(dir_path):
                print(f"{num}. {direct}")
                paths.append(dir_path)
                num += 1
    try:
        while True:
            index_file = int(input(" Choose The Theme: ").strip())
            if index_file not in list(range(1, num)):
                print_yellow(
                    f"Please, enter the number from the range {list(range(1, num))}"
                )
                continue
            return paths[index_file - 1]
    except:
        raise ValueError("Unknown file's number")


def choose_file(dir_path: str) -> str | None:

    print(" == All Available Dictionaries ==\n")

    paths = []
    num = 1
    for file in os.listdir(dir_path):
        full_path = os.path.join(dir_path, file)
        if os.path.isfile(full_path):
            print(f"{num}. {file}")
            paths.append(full_path)
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


def choose_format() -> int:
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


def choose_level() -> float | None:
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


def choose_mode(mode: int) -> str:
    dict_mode: dict[int, str] = {
        1: "Add New Words",
        2: "Practice a List",
        3: "Review Forgotten Words",
        4: "Practice a Category",
    }
    return dict_mode[mode]

