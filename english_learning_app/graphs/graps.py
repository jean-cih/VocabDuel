from english_learning_app.graphs.models import knowledge_statistics, path_graph
import os.path
from datetime import datetime, date
import re


def write_data(path: str, phrase: str):
    today = date.today()
    with open(path, "a", encoding="utf-8") as file:
        file.write(f"{phrase}: {today.strftime('%Y-%m-%d')}")


def find_date(path: str, title: str) -> str | None:
    pattern = title + r":\s\b\d{4}-\d{2}-\d{2}\b"
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            res = re.findall(pattern, line)
            if res:
                return res[0].split(":")[1]
    return None


def get_difference_between_days(date_occasion: str) -> int | None:
    try:
        date_obj = datetime.strptime(date_occasion, "%Y-%m-%d").date()
        today = date.today()
        return (today - date_obj).days
    except:
        return None


def fetch_data_from_file(path: str) -> None:
    # Извлечение данных из файла в словарь
    setup_date = find_date(path, "Setup Date")
    if setup_date:
        knowledge_statistics["Setup Date"] = setup_date.strip()

    days_after_setup = get_difference_between_days(knowledge_statistics["Setup Date"])

    entry_date = find_date(path, "Last Entry")
    if entry_date:
        knowledge_statistics["Last Entry"] = entry_date.strip()

    with open(path, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    list_data = re.findall(r"```chart\n(.*?)\n```", markdown_text, re.DOTALL)[:2]
    for graph_id, data in enumerate(list_data, 1):
        knowledge_statistics[f"graph{graph_id}"][1]["labels"] = [
            day + 1 for day in range(days_after_setup + 1)
        ]  # Генерация временной линии

        arrays = re.findall(r"data: \[(.*?)]", data)
        for series_id, array in enumerate(arrays, 1):
            knowledge_statistics[f"graph{graph_id}"][1][f"series{series_id}"][
                "    data"
            ] = [int(digit) for digit in array.split(",")]

    return None


def add_cards_in_dict(cards: int):
    # Добавление данных в словари
    days_after_last_entry = get_difference_between_days(
        knowledge_statistics["Last Entry"]
    )
    if days_after_last_entry > 0:
        # Добавляем
        del knowledge_statistics["graph1"][1]["series1"]["    data"][-1]
        knowledge_statistics["graph1"][1]["series1"]["    data"] += [0] * (
            days_after_last_entry - 1
        ) + [cards, 0]
    else:
        # Складываем
        knowledge_statistics["graph1"][1]["series1"]["    data"][-2] += cards

    knowledge_statistics["Total number of cards for all time"] = sum(
        knowledge_statistics["graph1"][1]["series1"]["    data"]
    )


def fetch_data_from_dict() -> str:
    # Извлечение данных из словаря в строку
    index_series = 0
    content = ""
    for graph, graph_value in knowledge_statistics.items():
        if isinstance(graph_value, list):
            content += f"\n### {graph_value[0]}\n"

            content += "```chart\n"
            for key, value in graph_value[1].items():
                if not isinstance(value, dict):
                    content += f"{key}: {value}\n"
                else:
                    if content[index_series:].find("series") == -1:
                        content += f"series:\n"
                    for series_key, series_value in value.items():
                        content += f"{series_key}: {series_value}\n"

            content += "```\n"
            index_series = len(content)
        else:
            content += f"\n**{graph}: {graph_value}\n"

    return content


def write_to_file(path: str, content: str):
    # Запись в файл
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def get_all_dicts_paths(path_dir: str) -> list[str]:
    paths = []
    for root, dirs, files in os.walk(path_dir):
        for file in files:
            paths.append(os.path.join(root, file))
    return paths


def get_number_words(path_dir: str) -> tuple[int, int]:
    paths = get_all_dicts_paths(path_dir)

    all_known_words = 0
    all_unknown_words = 0
    for path in paths:
        with open(path, "r") as file:
            for line in file:
                if not re.match(r"\d+\.", line):
                    continue
                index = line.find("🔥")
                if index == -1:
                    all_unknown_words += 1
                else:
                    all_known_words += 1

    return all_known_words, all_unknown_words


def get_unique_number_words(path_dir: str) -> tuple[int, int]:
    paths = get_all_dicts_paths(path_dir)

    unique_words = set()
    unique_known_words = set()
    for path in paths:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                if not re.match(r"\d+\.", line):
                    continue
                eng_word = re.search(r"[ 🔥]\*\*([^*]+)\*\*", line)
                if eng_word is not None:
                    unique_words.add(eng_word.group(1))
                    if eng_word.group().find("🔥") != -1:
                        unique_known_words.add(eng_word.group(1))

    return len(unique_words), len(unique_known_words)


def add_current_level_in_dict(unique_words: int, known_words: int) -> None:
    knowledge_statistics["Total number of all words"] = unique_words
    knowledge_statistics["Total number of known words"] = f"{known_words}🔥"

    days_after_setup = get_difference_between_days(knowledge_statistics["Last Entry"])
    if days_after_setup > 0:
        # Добавляем
        del knowledge_statistics["graph2"][1]["series1"]["    data"][-1]
        knowledge_statistics["graph2"][1]["series1"]["    data"] += [
            knowledge_statistics["graph2"][1]["series1"]["    data"][-1]
        ] * (days_after_setup - 1) + [unique_words - known_words, 0]

        del knowledge_statistics["graph2"][1]["series2"]["    data"][-1]
        knowledge_statistics["graph2"][1]["series2"]["    data"] += [
            knowledge_statistics["graph2"][1]["series2"]["    data"][-1]
        ] * (days_after_setup - 1) + [known_words, 0]
    else:
        # Переписываем
        knowledge_statistics["graph2"][1]["series1"]["    data"][-2] = (
            unique_words - known_words
        )
        knowledge_statistics["graph2"][1]["series2"]["    data"][-2] = known_words

    return None


def add_topics_in_dict(path: str):
    # Добавление данных в массив эрудиции
    knowledge_statistics["graph3"][1]["labels"] = sorted(
        knowledge_statistics["graph3"][1]["labels"]
    )
    knowledge_statistics["graph3"][1]["series1"]["    data"] = []

    for dir in sorted(knowledge_statistics["graph3"][1]["labels"]):
        dir_path = os.path.join(path, dir[:-2].strip())

        for root, dirs, files in os.walk(dir_path):
            sum_f_words = 0
            sum_u_words = 0
            for file in files:
                path_to_file = os.path.join(root, file)

                with open(path_to_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.find("Forgettable words") != -1:
                            f_words = int(line.split(": ")[1])
                            sum_f_words += f_words
                        if line.find("Understandable words") != -1:
                            u_words = int(line.split(": ")[1])
                            sum_u_words += u_words

            if sum_f_words == 0:
                knowledge_statistics["graph3"][1]["series1"]["    data"].append(0)
            else:
                knowledge_statistics["graph3"][1]["series1"]["    data"].append(
                    sum_u_words * 100 // (sum_u_words + sum_f_words)
                )


def draw_graph(cards: int, path_dir: str) -> None:

    fetch_data_from_file(path_graph)

    add_cards_in_dict(cards)

    unique_words, known_words = get_unique_number_words(path_dir)
    add_current_level_in_dict(unique_words, known_words)

    add_topics_in_dict(path_dir)

    content = fetch_data_from_dict()

    write_to_file(path_graph, content)
