import csv
import argparse
from pathlib import Path
from lab04.io_txt_csv import write_csv
from lab08.serialize import students_from_csv
from lab08.models import validate_student, STUDENT_FIELDS

DB_FILE = Path("data/lab09/students.csv")

def save_students(students, path=DB_FILE):
    with Path(path).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=STUDENT_FIELDS)
        writer.writeheader()
        writer.writerows(students)


def add_student(rec: dict, path=DB_FILE) -> None:
    validate_student(rec)
    students = students_from_csv(DB_FILE)
    students.append(rec)
    save_students(students, path=path)

def main():
    parser = argparse.ArgumentParser(description="Парсер для БД")
    sub_parser = parser.add_subparsers(dest="cmd")

    parser.add_argument("--db", dest="db", help="Путь к хранилищу")

    add = sub_parser.add_parser("Add student")
    add.add_argument("--fio", dest="fio", required=True, type=str, help="ФИО студента")
    add.add_argument("--birthdate", dest="birthdate", required=True, type=str, help="Дата рождения студента")
    add.add_argument("--group", dest="group", required=True, type=str, help="Группа студента")
    add.add_argument("--gpa", dest="gpa", required=True, type=float, help="GPA студента")

    args = parser.parse_args()

    if args.cmd == "Add student":
        new_student = {
            "fio": args.fio,
            "birthdate": args.birthdate,
            "group": args.group,
            "gpa": args.gpa
        }
        validate_student(rec=new_student)


if __name__ == "__main__":
    main()