def bubble_sort(nums: list[int | float]) -> list[int | float]:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > nums[j]:
                nums[i], nums[j] = nums[j], nums[i]
    return nums

print(bubble_sort([7,6,5,4,3,2,1]))
