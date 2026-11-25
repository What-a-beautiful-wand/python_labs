# ЛАБОРАТОРНАЯ РАБОТА №8

## ЗАДАНИЕ А — МОДЕЛЬ STUDENT

### ПРОВЕРКА ДАТЫ — VALIDATE_DATE

```python
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
```

Принимаем дату рождения строкой. Через `date.fromisoformat` проверяем существование даты, а сравнением с `isoformat()` — точный формат `YYYY-MM-DD`. Поэтому `2003-02-30`, запись без дефисов и будущая дата вызывают `ValueError` с причиной.

### ПРОВЕРКА ЗАПИСИ — VALIDATE_STUDENT

```python
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
```

Проверяем тип записи и сравниваем множества ключей, поэтому перестановка полей не считается ошибкой. ФИО и группа должны быть строками и оставаться непустыми после `strip()`. Оба текстовых поля должны кодироваться в UTF-8. Дату проверяем через `validate_date`.

GPA должен быть числом `int` или `float` в диапазоне 0…5. Отдельно исключаем `bool`, поскольку в Python он является подклассом `int`. Успешная проверка возвращает `None` и не изменяет запись; неверный тип вызывает `TypeError`, неверное значение — `ValueError`.

### СОЗДАНИЕ ЗАПИСИ — MAKE_STUDENT

```python
def make_student(fio: str, birthdate: str, group: str, gpa: int | float) -> dict:
    rec = {"fio": fio, "birthdate": birthdate, "group": group, "gpa": gpa}
    validate_student(rec)
    return {
        "fio": " ".join(fio.split()),
        "birthdate": birthdate,
        "group": group.strip(),
        "gpa": float(gpa),
    }
```

Собираем словарь и передаём его в `validate_student`, чтобы конструктор выполнял те же проверки, что и готовая запись. После проверки сохраняем все слова ФИО с одним пробелом между ними, обрезаем пробелы по краям группы и приводим GPA к `float`.

В `make_student` передаём числовой GPA, например `4.3` или `5`. Строку `"4.3"` здесь не принимаем: преобразование строк выполняется при импорте в `student_from_dict`.

### ПОЛНЫЙ ВОЗРАСТ — STUDENT_AGE

```python
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
```

Проверяем запись и разбираем дату рождения. Если `today` не передан, берём `date.today()`. Сначала вычисляем разницу лет, затем сравниваем кортежи `(месяц, день)`. Если день рождения ещё не наступил, уменьшаем возраст на единицу.

Например, для даты рождения `2007-09-20` на `2026-09-19` получаем 18 лет, а на `2026-09-20` — 19 лет. Переданная дата расчёта позволяет проверить эти случаи независимо от текущего дня. Дату раньше рождения отклоняем. Для родившегося 29 февраля в невисокосный год возраст увеличивается 1 марта.

### КРАСИВЫЙ ВЫВОД — FORMAT_STUDENT

```python
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
```

Разбиваем ФИО через `split()`, оставляем первое слово целиком и собираем инициалы остальных частей. Возраст получаем через `student_age`. Для чисел с последними двумя цифрами 11–14 выбираем `лет`; в остальных случаях по последней цифре выбираем `год`, `года` или `лет`. GPA выводим с двумя знаками после точки.

Получаем строку вида `Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30`. Возраст в этой строке зависит от текущей даты.

### КОПИЯ ДЛЯ СЕРИАЛИЗАЦИИ — STUDENT_TO_DICT

```python
def student_to_dict(rec: dict) -> dict:
    validate_student(rec)
    return rec.copy()
```

Проверяем запись и возвращаем `rec.copy()`. Значения сохраняются, но сам словарь получается новым: изменение GPA в копии не меняет исходную запись. Поверхностной копии достаточно, потому что поля содержат только строки и числа.

### ВОССТАНОВЛЕНИЕ ЗАПИСИ — STUDENT_FROM_DICT

```python
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
```

Принимаем словарь из внешнего источника и выбираем только ключи из `STUDENT_FIELDS`. Лишние поля не переносим, а при отсутствии обязательного поля вызываем `ValueError`, называя это поле.

При импорте преобразуем строковый GPA через `float()`. Функция `validate_student` проверяет тип и диапазон `0 <= gpa <= 5`. Границы включены. Точность ограничена типом `float`: например, `"5.0000000000000001"` округляется до `5.0` и проходит проверку.

## ЗАДАНИЕ Б — СЕРИАЛИЗАЦИЯ В JSON

Функции находятся в [serialize.py](serialize.py). Для импорта и записи используем следующие модули.

```python
import csv
import json
from pathlib import Path

from src.lab08.models import STUDENT_FIELDS, student_from_dict, validate_student
```

### СОХРАНЕНИЕ — STUDENTS_TO_JSON

```python
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
```

Принимаем список записей и путь типа `str` или `Path`. Проверяем каждую запись через `validate_student` и передаём исходный список в `json.dump`. Если запись неверна, сообщаем её номер и причину.

Пишем JSON в UTF-8 с отступом в два пробела во временный файл рядом с основным. У каждого сохранения своё имя файла, поэтому параллельные записи не мешают друг другу. После успешной записи и закрытия файла вызываем `replace()`. Если при записи закончится место на диске или оперативная память, прежний файл сохранится, а блок `finally` удалит временный.

### ЧТЕНИЕ — STUDENTS_FROM_JSON

```python
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
```

Читаем UTF-8 с BOM или без него. Дробные числа JSON сразу читаются как `float`. Функция `_unique_fields` проверяет пары ключей и значений каждого объекта и при повторе ключа вызывает `ValueError` с его именем. На верхнем уровне ожидаем массив, а каждый его элемент передаём в `student_from_dict`. Возвращаем список проверенных записей с GPA типа `float`. Пустой массив допустим и превращается в пустой список.

### JSON ДО И ПОСЛЕ ПРЕОБРАЗОВАНИЯ

Во входном файле [students_input.json](../../data/lab08/students_input.json) находятся две записи:

```json
[
  {
    "fio": "Иванов Иван Иванович",
    "birthdate": "2007-09-20",
    "group": "БИВТ-26-6-1",
    "gpa": "4.3"
  },
  {
    "fio": "Петрова Анна Сергеевна",
    "birthdate": "2008-03-08",
    "group": "БИВТ-26-6-1",
    "gpa": 5
  }
]
```

После чтения и сохранения в [students_output.json](../../data/lab08/students_output.json) получаем:

```json
[
  {
    "fio": "Иванов Иван Иванович",
    "birthdate": "2007-09-20",
    "group": "БИВТ-26-6-1",
    "gpa": 4.3
  },
  {
    "fio": "Петрова Анна Сергеевна",
    "birthdate": "2008-03-08",
    "group": "БИВТ-26-6-1",
    "gpa": 5.0
  }
]
```

Число записей и значения остальных полей сохраняются. Строковый GPA `"4.3"` становится числом `4.3`, а целое `5` — числом `5.0`. В обоих случаях в Python получаем `float`.

### ПРОВЕРКА НЕВЕРНЫХ ДАННЫХ

В файле [students_bad.json](../../data/lab08/students_bad.json) первая запись содержит несуществующую дату `2003-02-30`, а вторая — GPA `7`:

```json
[
  {
    "fio": "Иванов Иван Иванович",
    "birthdate": "2003-02-30",
    "group": "БИВТ-26-6-1",
    "gpa": "4.3"
  },
  {
    "fio": "Петрова Анна Сергеевна",
    "birthdate": "2008-03-08",
    "group": "БИВТ-26-6-1",
    "gpa": 7
  }
]
```

Политика `strict` останавливает чтение на ошибке даты первой записи. Если исправить эту дату, следующей ошибкой станет GPA второй записи. Демонстрация отдельно показывает оба нарушения, чтобы остановка на первой ошибке не скрывала проверку среднего балла.

```python
from pathlib import Path
from src.lab08.models import make_student
from src.lab08.serialize import students_from_json

try:
    students_from_json(Path("data/lab08") / "students_bad.json")
except ValueError as error:
    print(f"Чтение students_bad.json: ValueError: {error}")
for birthdate, gpa in (("2003-02-30", 4.3), ("2007-09-20", 7), ("2007-09-20", True)):
    try:
        make_student("Иванов Иван Иванович", birthdate, "БИВТ-26-6-1", gpa)
    except (TypeError, ValueError) as error:
        print(f"birthdate={birthdate}, gpa={gpa}: {type(error).__name__}: {error}")
```

Ошибку в записи из файла импорт сообщает как `ValueError` с номером записи. При прямом вызове функции тип исключения показывает, передан ли неверный тип или недопустимое значение.


### ОБНОВЛЕНИЕ ЗАПИСИ — UPDATE_STUDENT

```python
def update_student(rec: dict, **fields) -> dict:
    validate_student(rec)
    for field in fields:
        if field not in STUDENT_FIELDS:
            raise KeyError(field)
    updated = rec.copy()
    updated.update(fields)
    return make_student(**updated)
```

Проверяем исходную запись и названия изменяемых полей. Неизвестный ключ вызывает `KeyError`. Затем создаём копию, обновляем её поля через `update()` и передаём в `make_student` для проверки и нормализации значений. При неверном типе возникает `TypeError`, при недопустимом значении — `ValueError`. Обновление происходит в копии.

### ИМПОРТ ИЗ CSV — STUDENTS_FROM_CSV

```python
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
```

Читаем CSV в UTF-8 с BOM или без него. Параметр `newline=""` позволяет читать переносы строк внутри полей в кавычках. При незакрытой кавычке в конце файла `strict=True` останавливает импорт. Проверяем, что заголовок содержит ровно поля `fio`, `birthdate`, `group`, `gpa`, без пропущенных, лишних или повторяющихся названий. Порядок столбцов может отличаться. Для каждой записи проверяем число значений и вызываем `student_from_dict`.

Значения CSV приходят строками. Для GPA действует та же проверка диапазона, что и при чтении JSON. Если поле превышает лимит парсера или строка содержит неверные данные, получаем `ValueError` с причиной и номером записи. Нумерация начинается с 1 после заголовка. Ошибки разбора заголовка помечаются отдельно.

Входной файл [students_input.csv](../../data/lab08/students_input.csv) содержит:

```csv
fio,birthdate,group,gpa
Иванов Иван Иванович,2007-09-20,БИВТ-26-6-1,4.3
Петрова Анна Сергеевна,2008-03-08,БИВТ-26-6-1,5
```

### ПРИМЕР ОБНОВЛЕНИЯ И ИМПОРТА CSV

```python
from pathlib import Path
from src.lab08.models import make_student, update_student
from src.lab08.serialize import students_from_csv

student = make_student("Иванов Иван Иванович", "2007-09-20", "БИВТ-26-6-1", 4.3)
updated = update_student(student, gpa=4.8)
print("GPA исходной записи:", student["gpa"])
print("GPA обновлённой записи:", updated["gpa"])
print("Записи — один объект:", updated is student)
try:
    update_student(student, course=1)
except KeyError as error:
    print(f"Неизвестное поле: KeyError: {error}")
students = students_from_csv(Path("data/lab08") / "students_input.csv")
print("Прочитано из CSV:", len(students))
for rec in students:
    print(f"{rec['fio']}: GPA {rec['gpa']}, тип {type(rec['gpa']).__name__}")
```
