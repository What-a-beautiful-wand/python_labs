def format_record(rec: tuple[str, str, float]) -> str:

    try:
        name = rec[0]
        group = rec[1]
        gpa = rec[2]
    except IndexError:
        raise ValueError('Все поля должны быть заполнены')
    
    if name.__class__ != str:
        raise TypeError('Имя должно быть строкой')
    if group.__class__ != str:
        raise TypeError('Группа должна быть строкой')
    if gpa.__class__ != float and gpa.__class__ != int:
        raise TypeError('GPA должно быть числом')

    name = rec[0].title().split()

    try:
        name = f'{name[0]} {name[1][0]}.{name[2][0]}.'
    except IndexError:
        name = f'{name[0]} {name[1][0]}.'

    gpa = f'{round(gpa, 2):.2f}'

    return f'{name}, гр. {group}, GPA {gpa}'