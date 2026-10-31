def bubble_sort(nums: list[int | float]) -> list[int | float]:
    nums = list(nums)
    for end in range(len(nums) - 1, 0, -1):
        swapped = False
        for j in range(end):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:
            break
    return nums

def insertion_sort(nums: list[int | float]) -> list[int | float]:
    nums = list(nums)
    for i in range(1, len(nums)):
        current = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > current:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = current
    return nums

def selection_sort(nums: list[int | float]) -> list[int | float]:
    nums = list(nums)
    for i in range(len(nums) - 1):
        min_index = i
        for j in range(i +  1, len(nums)):
            if nums[j] < nums[min_index]:
                min_index = j
        nums[i], nums[min_index] = nums[min_index], nums[i]
    return nums
