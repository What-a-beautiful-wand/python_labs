from operator import itemgetter
from pathlib import Path

from src.lab04.io_txt_csv import write_csv
from src.lab08.models import STUDENT_FIELDS, validate_student, format_student
from src.lab08.serialize import students_from_csv

HEADER = STUDENT_FIELDS


def ensure_storage(path):
    path = Path(path)
    if not path.exists():
        save_students(path, [])


def load_students(path):
    return students_from_csv(path)


def save_students(path, students):
    rows = []
    for student in students:
        validate_student(student)
        rows.append(tuple(student[field] for field in HEADER))
    write_csv(rows, path, header=HEADER)


def list_students(path, sort_by=None, reverse=False):
    if sort_by not in (None, "fio", "gpa"):
        raise ValueError(f"Unknown sort field: {sort_by}")
    students = load_students(path)
    if sort_by is None:
        return students
    return sorted(students, key=itemgetter(sort_by), reverse=reverse)


def add_student(path, student):
    validate_student(student)
    students = load_students(path)
    fio = " ".join(student["fio"].split())
    for existing in students:
        if existing["fio"] == fio:
            raise ValueError(f"Студент с ФИО «{fio}» уже есть в базе")
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


def stats_student(path) -> dict:
    students = load_students(path)
    count = len(students)
    groups = {}
    top_students = []
    total_gpa = 0
    min_gpa = None
    for student in students:
        group = student["group"]
        groups[group] = groups.get(group, 0) + 1
        gpa = student["gpa"]
        total_gpa += gpa
        if min_gpa is None or gpa < min_gpa:
            min_gpa = gpa

        if len(top_students) < 5 or gpa > top_students[-1]["gpa"]:
            top_students.append(student)
            top_students.sort(key=lambda row: row["gpa"], reverse=True)
            del top_students[5:]
    return {
        "count": count,
        "min_gpa": min_gpa,
        "max_gpa": top_students[0]["gpa"] if top_students else None,
        "avg_gpa": f"{total_gpa / count:.2f}" if count else None,
        "groups": groups,
        "top_5_students": "".join(f"\n{format_student(student)}" for student in top_students),
    }
