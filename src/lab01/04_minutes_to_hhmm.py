minutes = int(input('Минуты: '))
if minutes > 1440:
    raise ValueError('Слишком много минут')
hours = minutes // 60
minutes = minutes - hours * 60
print(f'{hours}:{minutes}')