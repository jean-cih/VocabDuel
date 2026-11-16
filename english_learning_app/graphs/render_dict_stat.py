from english_learning_app.domain.dict_statistic import DictStats


def render_dict_stat(dict_stat: DictStats) -> str:
    content = "**Statistic:\n"

    content += f"- _The Number of page repetitions: {dict_stat.repetitions}\n"
    content += f"- _Average page comprehension (%): {dict_stat.average_comp}\n"
    content += f"- _The Number of 🤯 Forgettable words: {dict_stat.forgotten}\n"
    content += f"- _The Number of 🧠 Understandable words: {dict_stat.known}\n\n"

    return content
