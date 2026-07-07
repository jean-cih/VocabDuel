from datetime import date

path_graph = "../../../mnt/c/Работа/MyBrainObsidian/personal-obsidian-vault/English/Dictionaries/Knowledge statistics.md"

knowledge_statistics = {
    "graph1": [
        "Cards completed per day",
        {
            "type": "bar",
            "labels": [],  # Временная шкала
            "series1": {
                "  - label": "Words per day",
                "    data": [],  # Количество карточек за день
                "    backgroundColor": "rgba(32, 237, 132)",
            },
        },
    ],
    "graph2": [
        "Current level of knowledge",
        {
            "type": "bar",
            "labels": [],  # Временная шкала
            "series1": {
                "  - label": "Forgot / New",
                "    data": [],  # Количество незнакомых слов
                "    backgroundColor": "rgba(255, 94, 0)",
            },
            "series2": {
                "  - label": "Know",
                "    data": [],  # Количество известных слов
                "    backgroundColor": "rgba(32, 237, 132)",
            },
        },
        "",
    ],
    "graph3": [
        "Progress on Topics",
        {
            "type": "line",
            "labels": [
                "Movies 🎬",
                "Travel ✈️",
                "Food 🍕",
                "Music 🎵",
                "Work 💼",
                "Family ❤️",
                "Health 🏥",
                "Weather ☀️",
                "Clothes 👗",
                "Sport ⚽",
                "Technology 💻",
                "House 🏠",
                "Animal 🐶",
                "Body 💪",
                "Writing ✍️",
                "Speaking & Expressions 🗣️",
                "Books 📚",
            ],  # Различные темы
            "series1": {
                "  - label": "(%)",
                "    data": [],  # Процент понимания темы
                "    backgroundColor": "rgba(109, 40, 217)",
                "    borderColor": "rgba(32, 237, 132)",
                "    pointBackgroundColor": "rgba(32, 237, 132)",
                "    fill": "true",
            },
            "series2": {
                "  - label": "'Goal: 100%'",
                "    data": [
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                    100,
                ],  # Предел знаний в процентах
                "    backgroundColor": "rgba(0, 0, 0, 0)",
                "    borderColor": "rgba(32, 237, 132, 0.6)",
                "    borderDash": [8, 4],
                "    pointRadius": 0,
                "    fill": False,
                "    borderWidth": 2,
            },
        },
    ],
    "Total number of cards for all time": 0,
    "Total number of all words": 0,
    "Total number of known words": 0,
    "Setup Date": date.today().strftime("%Y-%m-%d"),
    "Last Entry": date.today().strftime("%Y-%m-%d"),
}
