n = int(input('in_1: '))
och, zaoch = 0, 0
for _ in range(2, n + 2):
    member = input(f'in_{_}: ').split()
    category = member[-1]
    if category == 'True':
        och += 1
    else:
        zaoch += 1
print(och, zaoch)