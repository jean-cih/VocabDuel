from fastapi import FastAPI, Body, status
from pathlib import Path
from typing import Dict, Tuple
import random
import re

folder_path = Path("../../data-base")


app = FastAPI()


@app.get("/dicts")
def get_all_dicts() -> Dict[int, str]:
    index = 0
    dict_names = {}
    for file_path in folder_path.rglob("*"):
        if file_path.is_file():
            dict_names[index] = file_path.name
            index += 1

    return dict_names


@app.get("/words/random")
def get_word_by_dict_id(dict_id: int) -> str:
    for index, file_path in enumerate(folder_path.rglob("*")):
        if index == dict_id:
            rand_index = random.randint(0, get_amount_words(file_path) - 1)
            with open(file_path, "r") as file:
                for index, line in enumerate(file):
                    if index == rand_index:
                        return line
            break


@app.get("/words")
def get_all_words(dict_id: int) -> Dict[int, Tuple[str, str]]:
    words = {}
    for index, file_path in enumerate(folder_path.rglob("*")):
        if index == dict_id:
            with open(file_path, "r", encoding="utf-8") as file:
                for index, line in enumerate(file):
                    eng_word = re.search(r"\*\*(.+?)\*\*", line)
                    trans_word = re.search(r"[\-–—]\s*(.*)$", line)
                    words[index] = (
                        eng_word.group(1).strip(),
                        trans_word.group(1).strip(),
                    )
            break

    return words


def get_amount_words(file_path: str):
    amount = 0
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line == "---":
                continue
            amount += 1

    return amount


@app.post("/words/add_word", status_code=201)
def add_word_in_dict(dict_id: int = Body(embed=True), word: list = Body(embed=True)):
    for index, file_path in enumerate(folder_path.rglob("*")):
        if index == dict_id:
            with open(file_path, "a") as file:
                new_line = (
                    f"\n{get_amount_words(file_path) + 1}. **{word[0]}** - {word[1]}"
                )
                file.write(new_line)
            break


@app.delete("/words/del_word", status_code=200)
def delete_word(dict_id: int = Body(embed=True), word_id: int = Body(embed=True)):
    new_lines = []
    for index, file_path in enumerate(folder_path.rglob("*")):
        if index == dict_id:
            with open(file_path, "r") as file:
                lines = file.readlines()

            for line in lines:
                if line.strip().startswith(f"{word_id}."):
                    new_line = line.replace(line, "")
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)

            with open(file_path, "w") as file:
                file.writelines(new_lines)

            break


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("game_controller:app", reload=True)
