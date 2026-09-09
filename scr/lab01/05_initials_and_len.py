full_name = input().split()
lenght = len(''.join(full_name))
name = ''.join([i[0].upper() for i in full_name])
print(f'Инициалы: {name}\nДлина: {lenght}')