import json
import datetime

STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")

def make_student(fio: str, birthdate: str, group: str, gpa: int | float) -> dict:
    if not isinstance(fio, str): raise ValueError('ФИО должно быть строкой')
    validate_date(birthdate)
    if not isinstance(group, str): raise ValueError('Группа должна быть строкой')
    try:
        gpa = float(gpa)
    except ValueError:
        raise ValueError('GPA должно быть числом')

    return {"fio":fio.strip(), "birthdate":birthdate, "group":group, "gpa":gpa}

def validate_date(date: str):
    datetime.date.fromisoformat(date)

def validate_student(rec: dict) -> None:
    if list(rec.keys()) != list(STUDENT_FIELDS):
        raise ValueError('Не все поля указаны')
    return
validate_student(make_student(fio='A', birthdate='2008-03-06', group='rqr', gpa='3'))    
#make_student(fio='A', birthdate='2008-03-06', group='rqr', gpa='3')