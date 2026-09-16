def format_record(rec: tuple[str, str, float]) -> str:

    name = rec[0].title().split()
    group = rec[1]
    gpa = rec[2]

    if not name or not group or not gpa:
        raise ValueError('Поля не должны быть пустыми')

    try:
        name = f'{name[0]} {name[1][0]}.{name[2][0]}.'
    except IndexError:
        name = f'{name[0]} {name[1][0]}.'

    gpa = f'{round(gpa, 2):.2f}'

    return f'{name}, гр. {group}, GPA {gpa}'

print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))