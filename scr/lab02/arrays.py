def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        raise ValueError('Пустой список не принимается')
    
    max_num, min_num = nums[0], nums[0]

    for number in nums:
        if max_num < number:
            max_num = number
        elif min_num > number:
            min_num = number

    return (min_num, max_num)

#============================================================================

def unique_sorted(nums: list[float | int]) -> list[float | int]:
    return sorted(list(set(nums)))

#============================================================================

def flatten(mat: list[list | tuple]) -> list:
    line = []
    for lst in mat:
        if lst.__class__ == list or lst.__class__ == tuple:
            line += lst
            
        else:
            raise TypeError('Такой тип недопустим')

    return line