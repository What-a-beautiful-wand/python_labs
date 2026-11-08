import csv
from operator import itemgetter
from pathlib import Path
from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student

HEADER = STUDENT_FIELDS


def ensure_storage(path):
    path = Path(path)
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=HEADER).writeheader()


def load_students(path):
    with Path(path).open("r", newline="", encoding="utf-8") as file:
        return [student_from_dict(row) for row in csv.DictReader(file)]


def save_students(path, students):
    with Path(path).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(students)


def list_students(path, sort_by=None):
    if sort_by not in (None, "fio", "gpa"):
        raise ValueError(f"Unknown sort field: {sort_by}")
    students = load_students(path)
    if sort_by is None:
        return students
    return sorted(students, key=itemgetter(sort_by))


def add_student(path, student):
    validate_student(student)
    students = load_students(path)
    students.append(student)
    save_students(path, students)


def find_students(path, substr):
    rows = load_students(path)
    substr = substr.casefold()
    return [r for r in rows if substr in r["fio"].casefold()]


def remove_student(path, fio):
    rows = load_students(path)
    remaining = [row for row in rows if row["fio"] != fio]
    removed = len(rows) - len(remaining)
    if removed:
        save_students(path, remaining)
    return removed


def update_student(path, fio, **fields):
    for field in fields:
        if field not in HEADER:
            raise KeyError(field)
    rows = load_students(path)
    for i, row in enumerate(rows):
        if row["fio"] == fio:
            updated = row.copy()
            updated.update(fields)
            validate_student(updated)
            rows[i] = updated
            save_students(path, rows)
            return True
    return False
