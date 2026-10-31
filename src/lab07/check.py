import random

from src.lab07.search import linear_search, binary_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

checks_count = 0

def check_search(trials = 100) -> None:
    global checks_count
    cases = [[], [4], [1, 2], [1, 1, 1, 5], [-5, 0 , 0 , 7]]

    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        cases.append(nums)

    for nums in cases:

        ordered = sorted(nums)
        targets = set(nums) | {-101, 101}

        for number in targets:
            try:
                expected = nums.index(number)
            except ValueError:
                expected = -1
            
            result = linear_search(nums, number)
            assert result == expected, (
                f'Ошибка в linear_search: {nums} target: {number}.'
                f'Ожидалось: {expected}, получено: {result}'
            )
            
            result = binary_search(ordered, number)
            if expected == -1:
                assert result == -1, (
                    f'binary_search нашла отсутствующее число: '
                    f'nums={ordered}, target={number}, result={result}'
                )
            else:
                assert 0 <= result < len(ordered), (
                    f'binary_search вернула неверный индекс: '
                    f'nums={ordered}, target={number}, result={result}'
                )
                assert ordered[result] == number, (
                    f'Ошибка в binary_search: nums={ordered}, '
                    f'target={number}, result={result}'
                )
                
    checks_count += len(cases)
    print(f'Проверка search прошла успешно. Проверено {len(cases)} тестов.')
    return None

#===================================================================================

def check_two_sum(trials = 100) -> None:
    global checks_count
    cases = [([], 0), ([3], 5), ([3, 3], 6), ([1, 2], 10), ([-3, 4, 2], -1)]
    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        target = random.randint(-200, 200)
        cases.append((nums, target))

    for nums, target in cases:
        brute = two_sum_brute(nums, target)
        fast = two_sum_fast(nums, target)

        assert (brute is None) == (fast is None), (
            f'Ошибка. nums: {nums}, target: {target}.'
            f'brute: {brute}, fast: {fast}'
        )

        for name, result in (("brute", brute), ("fast", fast)):
            if result is not None:
                i, j = result

                assert 0 <= i < j < len(nums), (
                    f'{name}: неверные индексы {result}, nums={nums}'
                )
                assert nums[i] + nums[j] == target, (
                    f'Ошибка {name}: неверная сумма {result}.'
                    f'nums: {nums}, target: {target}'
                )

    checks_count += len(cases)
    print(f'Проверка two_sum прошла успешно. Пройдено {len(cases)} тестов.')
    return None

#===================================================================================

def check_sorting(fn, trials = 100) -> None:
    global checks_count
    cases = [[], [5], [2, 2], [3, 2, 1], [-2, 0, -5, 0]]

    for _ in range(trials):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        cases.append(nums)

    for nums in cases:
        original = list(nums)
        expected = sorted(original)
        result = fn(nums)

        assert result == expected, (
            f'Ошибка в {fn.__name__}: {original}.'
            f'Ожидалось: {expected}, получено: {result}'
        )
        assert nums == original, (
            f'{fn.__name__} изменила исходный список {original}'
        )
        assert result is not nums, (
            f'{fn.__name__} должна возвращать новый список'
        )
    checks_count += len(cases)
    print(f'Проверка {fn.__name__} успешно пройдена. Пройдено: {len(cases)} тестов.')

if __name__ == "__main__":
    random.seed(67)
    check_search()
    check_two_sum()
    for fun in (bubble_sort, insertion_sort, selection_sort):
        check_sorting(fn=fun)
    print(f'OK: {checks_count} проверок')
