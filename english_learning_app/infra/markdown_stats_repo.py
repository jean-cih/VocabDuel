import os
import re
from english_learning_app.domain.knowledge_statistic import KnowledgeStats
from datetime import date, datetime
from english_learning_app.graphs.render_knowledge_stat import render


class MarkdownStatsRepository:
    def load(self, path: str) -> KnowledgeStats:
        date_format = "%Y-%m-%d"

        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        string_stats = re.findall(
            r"\*\*(.*?)\n", content, flags=re.DOTALL | re.IGNORECASE
        )
        setup_date = string_stats[3].split()[-1]
        last_entry = string_stats[4].split()[-1]

        inner_blocks = re.findall(
            r"```chart(.*?)```", content, flags=re.DOTALL | re.IGNORECASE
        )

        cards_per_day = self.parse_cards_per_day(inner_blocks[0])
        forgotten_per_day, known_per_day = self.parse_knowledge(inner_blocks[1])
        topics = self.parse_topics(inner_blocks[2])

        return KnowledgeStats(
            setup_date=datetime.strptime(setup_date, date_format).date(),
            last_entry=datetime.strptime(last_entry, date_format).date(),
            cards_per_day=cards_per_day,
            forgotten_per_day=forgotten_per_day,
            known_per_day=known_per_day,
            topics=topics,
        )

    @staticmethod
    def parse_cards_per_day(block: str) -> list[int]:
        content = block.split("\n")
        data = []
        for line in content:
            if "data" in line:
                raw_data = re.findall(
                    r"\[(.*?)]", line, flags=re.DOTALL | re.IGNORECASE
                )[0].split(",")
                data = [int(item) for item in raw_data]
        return data

    @staticmethod
    def parse_knowledge(block: str) -> list[list[int]]:
        content = block.split("\n")
        datas = []
        for line in content:
            if "data" in line:
                raw_data = re.findall(
                    r"\[(.*?)]", line, flags=re.DOTALL | re.IGNORECASE
                )[0].split(",")
                data = [int(item) for item in raw_data]
                datas.append(data)

        return datas

    @staticmethod
    def parse_topics(block: str) -> dict:
        content = block.split("\n")
        labels = []
        data = []
        for line in content:
            if "labels" in line:
                raw_labels = re.findall(
                    r"\[(.*?)]", line, flags=re.DOTALL | re.IGNORECASE
                )[0].split(",")
                labels = [label.strip() for label in raw_labels]
            elif "data" in line:
                raw_data = re.findall(
                    r"\[(.*?)]", line, flags=re.DOTALL | re.IGNORECASE
                )[0].split(",")
                data = [int(item) for item in raw_data]
                break

        return dict(zip(labels, data))

    def save(self, path: str, stats: KnowledgeStats) -> None:
        if os.path.isdir(path):
            raise IsADirectoryError(f"Cannot save statistics to a directory: {path}")

        with open(path, "w", encoding="utf-8") as file:
            content = render(stats)
            file.write(content)
