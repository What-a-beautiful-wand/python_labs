minutes = int(input('Минуты: '))
hours = minutes // 60
minutes = minutes - hours * 60
print(f'{hours}:{minutes}')