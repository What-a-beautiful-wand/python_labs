# Лабораторная Работа №2

### Задание 1

#### Функция 1

`def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    
    if not nums:
        raise ValueError('Пустой список не принимается')
    
    max_num, min_num = nums[0], nums[0]

    for number in nums:
        if max_num < number:
            max_num = number
        elif min_num > number:
            min_num = number

    return (min_num, max_num)`