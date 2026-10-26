import json
import csv
from pathlib import Path
from src.lib.io_txt_csv import write_csv

def json_to_csv(json_path: str, csv_path: str) -> None:
    if Path(json_path).suffix.lower() != ".json":
        raise ValueError("Входной файл должен быть JSON")
    if Path(csv_path).suffix.lower() != ".csv":
        raise ValueError("Выходной файл должен быть CSV")

    with open(json_path, mode='r', encoding='UTF-8') as file:
        text = json.load(file)

    if (
        not isinstance(text, list)
        or not text
        or not all(isinstance(item, dict) for item in text)
    ):
        raise ValueError("Пустой JSON")

    header = set()
    for item in text:
        for key in item:
            header.add(key)

    header = sorted(header)
    if not header:
        raise ValueError("JSON не содержит полей для CSV")
    if any(not key.strip() for key in header):
        raise ValueError("Названия полей JSON не должны быть пустыми")

    rows = []
    for item in text:
        row = []
        for key in header:
            row.append(item.get(key, ""))
        rows.append(row)

    write_csv(rows, csv_path, header=tuple(header))
        
#===================================================================

def csv_to_json(csv_path: str, json_path: str) -> None:
    if Path(csv_path).suffix.lower() != ".csv":
        raise ValueError("Входной файл должен быть CSV")
    if Path(json_path).suffix.lower() != ".json":
        raise ValueError("Выходной файл должен быть JSON")

    with open(csv_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        keys = next(reader, None)

        if not keys or any(not key.strip() for key in keys):
            raise ValueError("CSV пустой или отсутствует заголовок")
        if len(set(keys)) != len(keys):
            raise ValueError("Названия колонок CSV не должны повторяться")

        text = []
        for row in reader:
            text.append(dict(zip(keys, row, strict=True)))

    Path(json_path).parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(text, file, ensure_ascii=False, indent=2)
