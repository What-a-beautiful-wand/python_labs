n = int(input())
och, zaoch = 0, 0
for _ in range(n):
    member = input().split()
    category = member[-1]
    if category == 'True':
        och += 1
    else:
        zaoch += 1
print(och, zaoch)