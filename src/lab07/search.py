def linear_search(nums: list[int | float], x: int | float) -> int:
    for index in range(len(nums)):
        if nums[index] == x:
            return index
    return -1

def binary_search(sorted_nums: list[int | float], x) -> int:
    low = 0
    higth = len(sorted_nums) - 1
    while low <= higth:
        middle = (low + higth) // 2
        if sorted_nums[middle] == x:
            return middle
        elif sorted_nums[middle] < x:
            low = middle + 1
        else:
            higth = middle - 1
    return -1

def two_sum_brute(nums: list[int | float], target: int | float) -> tuple[int, int] | None:
    for first in range(len(nums)):
        for second in range(first + 1, len(nums)):
            if nums[first] + nums[second] == target:
                return (first, second)
    return None

def two_sum_fast(nums: list[int | float], target: int | float) -> tuple[int, int] | None:
    seens = {}
    for j, x in enumerate(nums):
        need = target - x
        if need in seens:
            return (seens[need], j)
        seens[x] = j
    return None
