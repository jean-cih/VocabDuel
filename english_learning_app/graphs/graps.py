from english_learning_app.graphs.models import knowledge_statistics, path_graph
import os.path
from datetime import datetime, date
import re


def write_data(path: str, phrase: str):
    today = date.today()
    with open(path, "a", encoding="utf-8") as file:
        file.write(f"{phrase}: {today.strftime('%Y-%m-%d')}")


def find_date(path: str) -> list:
    pattern = r"\b\d{4}-\d{2}-\d{2}\b"
    dates = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            res = re.findall(pattern, line)
            if res:
                dates.append(re.findall(pattern, line)[0])

    return dates


def get_difference_between_days(path: str, type: int):
    dates = find_date(path)
    try:
        date_obj = datetime.strptime(dates[type], "%Y-%m-%d").date()
        today = date.today()
        return (today - date_obj).days
    except:
        return None


def fetch_data_from_file(path: str) -> None:
    # Извлечение данных из файла в словарь
    diff_setup = get_difference_between_days(path, 0)
    if diff_setup is None:
        write_data(path, "**Setup Date")
        diff_setup = 0

    last_entry = get_difference_between_days(path, 1)
    if last_entry is None:
        write_data(path, "_Last Entry")

    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    pattern = r"\[!(.*?)!\]"
    list_data = re.findall(pattern, text)

    for index_label, data in enumerate(list_data, 1):
        arrays = data.split("&")
        knowledge_statistics[f"graph{index_label}"]["labels"] = [
            day + 1 for day in range(diff_setup + 1)
        ]
        for index_data, pair in enumerate(zip(arrays[::2], arrays[1::2]), 1):
            knowledge_statistics[f"graph{index_label}"][f"series{index_data}"][
                pair[0]
            ] = [int(digit) for digit in pair[1].split(",") if digit != ""]


def add_cards_in_dict(path: str, cards: int):
    # Добавление данных в словари
    last_entry_date = get_difference_between_days(path, 1)
    if last_entry_date > 0:
        # Добавляем
        del knowledge_statistics["graph1"]["series1"]["    data"][-1]
        knowledge_statistics["graph1"]["series1"]["    data"] += [0] * (
            last_entry_date - 1
        ) + [cards, 0]
    else:
        # Складываем
        knowledge_statistics["graph1"]["series1"]["    data"][-2] += cards


def fetch_data_from_dict(path: str) -> str:
    # Извлечение данных из словаря в строку
    index_series = 0
    content = ""
    invisible_data = ""
    for _, graph_value in knowledge_statistics.items():
        for key, value in graph_value.items():

            if key == "title":
                content += f"### {value}\n```chart\n"
                continue
            if not isinstance(value, dict):
                content += f"{key}: {value}\n"
            else:
                if content[index_series:].find("series") == -1:
                    content += f"series:\n"
                for subkey, subvalue in value.items():
                    content += f"{subkey}: {subvalue}\n"
                    if subkey == "    data":
                        invisible_data += f"{subkey}&{str(subvalue)[1:-1]}&"

        content += "```\n"
        index_series = len(content)

        content += f"> [!{invisible_data}!] Graphs data\n"
        invisible_data = ""

    content += f"\n**Setup Date: {find_date(path)[0]}**\n"
    content += f"\n_Last Entry: {date.today()}\n"

    return content


def write_to_file(path: str, content: str):
    # Запись в файл
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def get_number_words(path_dir: str) -> tuple[int, int]:
    paths = []
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            paths.append(os.path.join(root, file))

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

    return all_known_words, all_unknown_words


def add_current_level_in_dict(path_dir: str, path: str) -> None:

    known, unknown = get_number_words(path_dir)

    last_entry_date = get_difference_between_days(path, 1)
    if last_entry_date > 0:
        # Добавляем
        del knowledge_statistics["graph2"]["series1"]["    data"][-1]
        knowledge_statistics["graph2"]["series1"]["    data"] += [
            knowledge_statistics["graph2"]["series1"]["    data"][-1]
        ] * (last_entry_date - 1) + [unknown, 0]

        del knowledge_statistics["graph2"]["series2"]["    data"][-1]
        knowledge_statistics["graph2"]["series2"]["    data"] += [
            knowledge_statistics["graph2"]["series2"]["    data"][-1]
        ] * (last_entry_date - 1) + [known, 0]
    else:
        # Переписываем
        knowledge_statistics["graph2"]["series1"]["    data"][-2] = unknown
        knowledge_statistics["graph2"]["series2"]["    data"][-2] = known

    return None


def draw_graph(cards: int, path_dir: str) -> None:

    fetch_data_from_file(path_graph)

    add_cards_in_dict(path_graph, cards)
    add_current_level_in_dict(path_dir, path_graph)

    content = fetch_data_from_dict(path_graph)

    write_to_file(path_graph, content)
