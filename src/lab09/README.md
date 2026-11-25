# ЛАБОРАТОРНАЯ РАБОТА №9

## ЗАДАНИЕ А — ХРАНИЛИЩЕ CSV И CRUD

### СОЗДАНИЕ И ЧТЕНИЕ — ENSURE_STORAGE И LOAD_STUDENTS

```python
def ensure_storage(path):
    path = Path(path)
    if not path.exists():
        save_students(path, [])


def load_students(path):
    return students_from_csv(path)
```

Если файла ещё нет, сохраняем только заголовок `fio,birthdate,group,gpa`. При чтении используем `students_from_csv` из [ЛР8](../lab08/README.md). Она проверяет заголовок и каждую запись. GPA из CSV преобразуется из строки в число, чтобы сравнивать и сортировать оценки численно.

### СОХРАНЕНИЕ — SAVE_STUDENTS

```python
def save_students(path, students):
    rows = []
    for student in students:
        validate_student(student)
        rows.append(student.copy())

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    new_path = path.with_name(path.name + ".new")
    new_file = new_path.open("x", encoding="utf-8", newline="")
    try:
        with new_file:
            writer = csv.DictWriter(new_file, fieldnames=HEADER)
            writer.writeheader()
            writer.writerows(rows)
        new_path.replace(path)
    except BaseException:
        new_path.unlink(missing_ok=True)
        raise
```

Проверяем записи, создаём нужный каталог и записываем весь список через `csv.DictWriter` в соседний файл `students.csv.new`. Режим `"x"` сообщает об ошибке, если такой файл уже есть. После успешной записи и закрытия файла заменяем им основной CSV. При исключении во время записи или замены удаляем созданный `.new` и передаём ошибку дальше. Этот способ применяется и при создании базы, и при добавлении, обновлении или удалении записей.

### ДОБАВЛЕНИЕ, СПИСОК И ПОИСК

- `add_student` проверяет новую запись и добавляет её в конец списка. При проверке дубликатов убирает лишние пробелы в новом ФИО. Совпадение вызывает `ValueError`.
- `list_students` сохраняет порядок CSV по умолчанию, а при `sort_by="fio"` или `sort_by="gpa"` возвращает отсортированный список.
- `find_students` приводит запрос и ФИО к одному регистру через `casefold()` и возвращает все записи с подходящей подстрокой.

### ОБНОВЛЕНИЕ И УДАЛЕНИЕ — UPDATE_STUDENT И REMOVE_STUDENT

```python
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
```

В `**fields` передаём поля, которые нужно изменить. Неизвестный ключ вызывает `KeyError`. Для первого точного совпадения по ФИО копируем запись, применяем изменения и проверяем результат перед сохранением. Если совпадений нет, возвращаем `False`. `remove_student` удаляет все точные совпадения и возвращает их количество. Если удалять нечего, файл не перезаписывается.

## ЗАДАНИЕ Б — КОМАНДНАЯ СТРОКА

В [cli_students.py](cli_students.py) разбираем аргументы через `argparse`. По умолчанию используется [students.csv](../../data/lab09/students.csv). Чтобы выбрать другой файл, указываем `--db` перед подкомандой. При обновлении передаём только заданные поля, поэтому, например, `--gpa 0` сохраняется как допустимое значение.

### СТАТИСТИКА — STATS_STUDENT

Команда `stats` показывает количество студентов, минимум, максимум и среднее GPA, число студентов по группам и до пяти лучших записей. При обходе списка накапливаем сумму GPA и увеличиваем счётчики групп. Топ поддерживаем в порядке убывания GPA. В топе возвращаем словари с ФИО и баллом, среднее в текущей реализации форматируем строкой с двумя знаками. Для пустой базы минимум, максимум и среднее равны `None`.

### ПРИМЕР РАБОТЫ

Запускаем команды из корня проекта. Для примера создаём отдельный `students-demo.csv` с одной записью.

```csv
fio,birthdate,group,gpa
Петрова Анна Сергеевна,2007-03-08,БИВТ-26-6-2,4.0
```

```text
$ python -m src.lab09.cli_students --db students-demo.csv add --fio 'Иванов Иван Иванович' --birthdate 2007-09-20 --group 'БИВТ-26-6-1' --gpa 4.3
Добавлен студент
Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30

$ python -m src.lab09.cli_students --db students-demo.csv list --sort gpa
Петрова А.С. (БИВТ-26-6-2), 19 лет, GPA 4.00
Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30

$ python -m src.lab09.cli_students --db students-demo.csv find --q 'ИВАНОВ'
Иванов И.И. (БИВТ-26-6-1), 19 лет, GPA 4.30

$ python -m src.lab09.cli_students --db students-demo.csv update --fio 'Иванов Иван Иванович' --gpa 4.8
Студент обновлён

$ python -m src.lab09.cli_students --db students-demo.csv remove --fio 'Петрова Анна Сергеевна'
Удалено: 1

$ python -m src.lab09.cli_students --db students-demo.csv stats
count: 1
min_gpa: 4.8
max_gpa: 4.8
avg_gpa: 4.80
groups: {'БИВТ-26-6-1': 1}
top_5_students: [{'fio': 'Иванов Иван Иванович', 'gpa': 4.8}]
```

### ИТОГОВЫЙ CSV

```csv
fio,birthdate,group,gpa
Иванов Иван Иванович,2007-09-20,БИВТ-26-6-1,4.8
```

### ПРОВЕРКА НЕВЕРНЫХ ДАННЫХ

Команда `update --fio "Иванов Иван Иванович" --gpa 6` вызывает `ValueError`, так как GPA должен быть от 0 до 5. После ошибки в CSV остаётся GPA `4.8`. В текущем CLI исключение выводится с traceback.
