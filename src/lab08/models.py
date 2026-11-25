import datetime


STUDENT_FIELDS = ("fio", "birthdate", "group", "gpa")


def validate_date(birthdate: str) -> None:
    if not isinstance(birthdate, str):
        raise TypeError(f"birthdate: ожидалась строка YYYY-MM-DD, получено {birthdate!r}")
    try:
        value = datetime.date.fromisoformat(birthdate)
    except ValueError:
        raise ValueError(f"birthdate: ожидалась существующая дата YYYY-MM-DD, получено {birthdate!r}") from None
    if value.isoformat() != birthdate:
        raise ValueError(f"birthdate: ожидался формат YYYY-MM-DD, получено {birthdate!r}")
    if value > datetime.date.today():
        raise ValueError(f"birthdate: ожидалась дата не позднее сегодняшней, получено {birthdate!r}")


def validate_student(rec: dict) -> None:
    if not isinstance(rec, dict):
        raise TypeError(f"Запись студента: ожидался словарь, получено {type(rec).__name__}")
    if set(rec) != set(STUDENT_FIELDS):
        raise ValueError("Нужны ровно поля fio, birthdate, group, gpa")
    for field in ("fio", "group"):
        value = rec[field]
        if not isinstance(value, str):
            raise TypeError(f"{field}: ожидалась строка, получено {value!r}")
        if not value.strip():
            raise ValueError(f"{field}: ожидалась непустая строка, получено {value!r}")
        try:
            value.encode("utf-8")
        except UnicodeEncodeError:
            raise ValueError(f"Поле {field} содержит недопустимый символ Unicode") from None
    validate_date(rec["birthdate"])
    gpa = rec["gpa"]
    if isinstance(gpa, bool) or not isinstance(gpa, (int, float)):
        raise TypeError(f"GPA: ожидалось число, получено {gpa!r}")
    if not 0 <= gpa <= 5:
        raise ValueError(f"GPA: ожидалось число от 0 до 5, получено {gpa!r}")


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
        raise TypeError(f"today: ожидалась дата, получено {today!r}")
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    if age < 0:
        raise ValueError("Дата расчёта возраста не может быть раньше даты рождения")
    return age


def format_student(rec: dict) -> str:
    age = student_age(rec)
    parts = rec["fio"].split()
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
        raise TypeError(f"Запись студента: ожидался словарь, получено {type(d).__name__}")
    try:
        rec = {field: d[field] for field in STUDENT_FIELDS}
    except KeyError as error:
        raise ValueError(f"Не указано поле {error.args[0]}") from None
    gpa = rec["gpa"]
    if isinstance(gpa, str):
        try:
            rec["gpa"] = float(gpa)
        except ValueError:
            raise ValueError(f"GPA: ожидалась числовая запись, получено {gpa!r}") from None
    return make_student(**rec)


def update_student(rec: dict, **fields) -> dict:
    validate_student(rec)
    for field in fields:
        if field not in STUDENT_FIELDS:
            raise KeyError(field)
    updated = rec.copy()
    updated.update(fields)
    return make_student(**updated)
