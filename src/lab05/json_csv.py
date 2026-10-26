import json
import csv
from src.lib.io_txt_csv import write_csv

def json_to_csv(json_path: str, csv_path: str) -> None:
    with open(json_path, mode='r', encoding='UTF-8') as file:
        text = json.load(file)

    if not text:
        raise ValueError("Пустой JSON")

    header = set()
    for item in text:
        for key in item:
            header.add(key)

    header = sorted(header)

    rows = []
    for item in text:
        row = []
        for key in header:
            row.append(item.get(key, ""))
        rows.append(row)

    write_csv(rows, csv_path, header=tuple(header))
        
#===================================================================

def csv_to_json(csv_path: str, json_path: str) -> None:
    with open(csv_path, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        keys = next(reader, None)

        if keys == None:
            raise ValueError("CSV пустой или отсутствует заголовок")

        text = []
        for row in reader:
            text.append(dict(zip(keys, row, strict=True)))

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(text, file, ensure_ascii=False, indent=2)
