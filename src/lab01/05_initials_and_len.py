full_name = input('ФИО: ').split()
lenght = len(''.join(full_name))+2
name = ''.join([i[0].upper() for i in full_name]) + '.'
print(f'Инициалы: {name}\nДлина: {lenght}')