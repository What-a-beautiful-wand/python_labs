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
    if not isinstance(rec, dict) or set(rec) != set(STUDENT_FIELDS):
        raise ValueError('Нужны ровно поля fio, birthdate, group, gpa')
    if not isinstance(rec["fio"], str) or not rec["fio"].strip():
        raise ValueError('ФИО должно быть непустой строкой')
    if not isinstance(rec["group"], str) or not rec["group"].strip():
        raise ValueError('Группа должна быть непустой строкой')
    if not isinstance(rec["birthdate"], str):
        raise ValueError('Дата рождения должна быть строкой YYYY-MM-DD')
    try:
        birthdate = datetime.date.fromisoformat(rec["birthdate"])
    except ValueError:
        raise ValueError('Дата рождения должна существовать и иметь формат YYYY-MM-DD') from None
    if birthdate.isoformat() != rec["birthdate"]:
        raise ValueError('Дата рождения должна иметь формат YYYY-MM-DD')
    if birthdate > datetime.date.today():
        raise ValueError('Дата рождения не может быть в будущем')
    gpa = rec["gpa"]
    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise ValueError('GPA должно быть числом')
    if not (0 <= gpa <= 5):
        raise ValueError('GPA должно быть от 0 до 5')


def student_age(rec: dict, today=None) -> int:
    birthdate = datetime.date.fromisoformat(rec["birthdate"])
    if today is None: today = datetime.date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day): age -= 1
    return age

def student_to_dict(rec: dict) -> dict:
    validate_student(rec)
    return rec.copy()


def student_from_dict(d: dict) -> dict:
    if not isinstance(d, dict):
        raise ValueError('Данные студента должны быть словарём')
    try:
        rec = {field: d[field] for field in STUDENT_FIELDS}
    except KeyError as error:
        raise ValueError(f'Не указано поле {error.args[0]}') from None
    if isinstance(rec["gpa"], bool) or not isinstance(rec["gpa"], (int, float, str)):
        raise ValueError('GPA должно быть числом')
    try:
        rec["gpa"] = float(rec["gpa"])
    except (TypeError, ValueError, OverflowError):
        raise ValueError('GPA должно быть числом') from None
    validate_student(rec)
    return rec


def format_student(rec: dict) -> str:
    fio = rec["fio"]
    name = ''.join([i[0].upper() for i in fio]) + '.'
    age, suffix = student_age(rec=rec), "лет"
    if 11 <= age % 100 <= 14: suffix = "лет"
    elif age % 10 == 1: suffix = "год"
    elif 2 <= age % 10 <= 4: suffix = "года"
    return f"{name}, ({rec["group"]}), {age} {suffix}, GPA {rec["gpa"]:.2f}"