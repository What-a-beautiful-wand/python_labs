import argparse
import csv
import sys
from pathlib import Path

from src.lab08.models import format_student
from src.lab09.group import (
    add_student,
    ensure_storage,
    find_students,
    list_students,
    remove_student,
    update_student,
    stats_student
)

DB_FILE = Path("data/lab09/students.csv")


def main():
    parser = argparse.ArgumentParser(description="База данных студентов")
    parser.add_argument("--db", type=Path, default=DB_FILE, help="Путь к хранилищу")
    sub_parser = parser.add_subparsers(dest="cmd", required=True)

    add = sub_parser.add_parser("add")
    add.add_argument("--fio", required=True, help="ФИО студента")
    add.add_argument("--birthdate", required=True, help="Дата рождения YYYY-MM-DD")
    add.add_argument("--group", required=True, help="Группа студента")
    add.add_argument("--gpa", required=True, type=float, help="GPA студента")

    list_student = sub_parser.add_parser("list")
    list_student.add_argument("--sort", dest="key", help="Ключ сортировки: fio или gpa")
    list_student.add_argument("-rev", action="store_true", default=False, help="Обратный порядок")

    find = sub_parser.add_parser("find")
    find.add_argument("--q", required=True, help="Подстрока в ФИО")

    remove = sub_parser.add_parser("remove")
    remove.add_argument("--fio", required=True, help="ФИО студента")

    update = sub_parser.add_parser("update")
    update.add_argument("--fio", required=True, help="ФИО студента")
    update.add_argument("--gpa", type=float, help="Новый GPA")
    update.add_argument("--group", help="Новая группа")
    update.add_argument("--birthdate", help="Новая дата рождения YYYY-MM-DD")

    stats = sub_parser.add_parser("stats")

    args = parser.parse_args()


    ensure_storage(args.db)
    if args.cmd == "add":
        new_student = {
            "fio": args.fio,
            "birthdate": args.birthdate,
            "group": args.group,
            "gpa": args.gpa,
        }
        add_student(args.db, new_student)
        print("Добавлен студент")
        print(format_student(new_student))

    elif args.cmd == "list":
        for student in list_students(args.db, sort_by=args.key, reverse=args.rev):
            print(format_student(student))

    elif args.cmd == "find":
        for student in find_students(args.db, args.q):
            print(format_student(student))
                
    elif args.cmd == "remove":
        print(f"Удалено: {remove_student(args.db, args.fio)}")
            
    elif args.cmd == "update":
        fields = {
            field: getattr(args, field)
            for field in ("gpa", "group", "birthdate")
            if getattr(args, field) is not None
        }
        if not fields:
            raise ValueError("Укажите хотя бы одно поле для обновления")
        if update_student(args.db, args.fio, **fields):
            print("Студент обновлён")
        else:
            print("Студент не найден")

    elif args.cmd == "stats":
        stat = stats_student(args.db)
        for key in stat:
            print(f"{key}: {stat[key]}")


if __name__ == "__main__": 
    main()