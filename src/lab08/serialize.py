import csv
import json
from pathlib import Path

from src.lab08.models import STUDENT_FIELDS, student_from_dict, student_to_dict


def students_to_json(students: list[dict], path: str | Path) -> None:
    if not isinstance(students, list):
        raise ValueError("Студенты должны быть списком записей")
    data = []
    for number, student in enumerate(students, start=1):
        try:
            data.append(student_to_dict(student))
        except ValueError as error:
            raise ValueError(f"Запись №{number}: {error}") from error
    output = json.dumps(data, ensure_ascii=False, indent=2)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(output, encoding="utf-8")


def students_from_json(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать массив записей студентов")
    students = []
    for number, item in enumerate(data, start=1):
        try:
            students.append(student_from_dict(item))
        except ValueError as error:
            raise ValueError(f"Запись №{number}: {error}") from error
    return students


def students_from_csv(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames
        if header is None or len(header) != len(STUDENT_FIELDS) or set(header) != set(STUDENT_FIELDS):
            raise ValueError("CSV должен содержать столбцы fio,birthdate,group,gpa")
        students = []
        for number, row in enumerate(reader, start=1):
            try:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError("Число значений не совпадает с числом столбцов")
                students.append(student_from_dict(row))
            except ValueError as error:
                raise ValueError(f"Запись №{number}: {error}") from error
    return students
