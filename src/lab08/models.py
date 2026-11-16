import datetime


STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def validate_date(birthdate: str) -> None:
    if not isinstance(birthdate, str):
        raise ValueError("Дата рождения должна быть строкой YYYY-MM-DD")
    try:
        value = datetime.date.fromisoformat(birthdate)
    except ValueError:
        raise ValueError("Дата рождения должна существовать и иметь формат YYYY-MM-DD") from None
    if value.isoformat() != birthdate:
        raise ValueError("Дата рождения должна иметь формат YYYY-MM-DD")
    if value > datetime.date.today():
        raise ValueError("Дата рождения не может быть в будущем")


def validate_student(rec: dict) -> None:
    if not isinstance(rec, dict) or set(rec) != set(STUDENT_FIELDS):
        raise ValueError("Нужны ровно поля fio, birthdate, group, gpa")
    if not isinstance(rec["fio"], str) or not rec["fio"].strip():
        raise ValueError("ФИО должно быть непустой строкой")
    if not isinstance(rec["group"], str) or not rec["group"].strip():
        raise ValueError("Группа должна быть непустой строкой")
    validate_date(rec["birthdate"])
    gpa = rec["gpa"]
    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise ValueError("GPA должно быть числом")
    if not 0 <= gpa <= 5:
        raise ValueError("GPA должно быть от 0 до 5")


def make_student(fio: str, birthdate: str, group: str, gpa: int | float) -> dict:
    rec = {"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa}
    validate_student(rec)
    return {
        "fio": " ".join(fio.split()),
        "birthdate": birthdate,
        "group": group.strip(),
        "gpa": float(gpa),
    }


def student_age(rec: dict, today=None) -> int:
    validate_student(rec)
    birthdate = datetime.date.fromisoformat(rec["birthdate"])
    if today is None:
        today = datetime.date.today()
    if not isinstance(today, datetime.date):
        raise ValueError("today должна быть датой")
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    if age < 0:
        raise ValueError("Дата расчёта возраста не может быть раньше даты рождения")
    return age


def format_student(rec: dict) -> str:
    age = student_age(rec)
    parts = rec["fio"].split()[:3]
    initials = "".join(part[0].upper() + "." for part in parts[1:])
    name = f"{parts[0]} {initials}".strip()
    if 11 <= age % 100 <= 14:
        suffix = "лет"
    elif age % 10 == 1:
        suffix = "год"
    elif 2 <= age % 10 <= 4:
        suffix = "года"
    else:
        suffix = "лет"
    return f"{name} ({rec['group']}), {age} {suffix}, GPA {rec['gpa']:.2f}"


def student_to_dict(rec: dict) -> dict:
    validate_student(rec)
    return rec.copy()


def student_from_dict(d: dict) -> dict:
    if not isinstance(d, dict):
        raise ValueError("Данные студента должны быть словарём")
    try:
        rec = {field: d[field] for field in STUDENT_FIELDS}
    except KeyError as error:
        raise ValueError(f"Не указано поле {error.args[0]}") from None
    if isinstance(rec["gpa"], bool) or not isinstance(rec["gpa"], (int, float, str)):
        raise ValueError("GPA должно быть числом")
    try:
        rec["gpa"] = float(rec["gpa"])
    except (TypeError, ValueError, OverflowError):
        raise ValueError("GPA должно быть числом") from None
    return make_student(**rec)


def update_student(rec: dict, **fields) -> dict:
    validate_student(rec)
    for field in fields:
        if field not in STUDENT_FIELDS:
            raise KeyError(field)
    updated = rec.copy()
    updated.update(fields)
    return make_student(**updated)
