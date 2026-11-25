import csv
import json
from pathlib import Path

from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student


def students_to_json(students: list[dict], path: str | Path) -> None:
    if not isinstance(students, list):
        raise TypeError(f"students: ожидался список, получено {type(students).__name__}")
    for number, student in enumerate(students, start=1):
        try:
            validate_student(student)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Запись №{number}: {error}") from error
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = [student_to_dict(student) for student in students]
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)



def _unique_fields(pairs: list[tuple]) -> dict:
    fields = {}
    for key, value in pairs:
        if key in fields:
            raise ValueError(f"Повторяющийся ключ JSON: {key}")
        fields[key] = value
    return fields


def students_from_json(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8-sig") as file:
        data = json.load(file, object_pairs_hook=_unique_fields)
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать массив записей студентов")
    students = []
    for number, item in enumerate(data, start=1):
        try:
            students.append(student_from_dict(item))
        except (TypeError, ValueError) as error:
            raise ValueError(f"Запись №{number}: {error}") from error
    return students


def students_from_csv(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, strict=True)
        try:
            header = reader.fieldnames or []
        except csv.Error as error:
            raise ValueError(f"Заголовок CSV: {error}") from error
        if len(header) != len(STUDENT_FIELDS) or set(header) != set(STUDENT_FIELDS):
            raise ValueError("CSV должен содержать столбцы fio,birthdate,group,gpa")
        students = []
        try:
            for row in reader:
                if None in row or None in row.values():
                    raise ValueError("Число значений не совпадает с числом столбцов")
                students.append(student_from_dict(row))
        except (csv.Error, TypeError, ValueError) as error:
            raise ValueError(f"Запись №{len(students) + 1}: {error}") from error
    return students
