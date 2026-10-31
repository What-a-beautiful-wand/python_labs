import argparse
import random
import signal
import timeit
from math import isfinite
from pathlib import Path

from src.lab04.io_txt_csv import write_csv
from src.lab07.search import binary_search, linear_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort


HEADER = ("task", "n", "impl", "seconds")
SORT_SIZES = (1_000, 10_000, 100_000)
TWO_SUM_SIZES = (1_000, 10_000)
SEARCH_SIZE = 100_000
SEARCH_QUERIES = 10_000


#===============================================================================

def measure_sort(fn, data, timeout=60):
    if not isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout должен быть положительным конечным числом")

    def stop_sorting(signum, frame):
        raise TimeoutError("Превышен лимит времени сортировки")

    previous_handler = signal.signal(signal.SIGALRM, stop_sorting)
    try:
        signal.setitimer(signal.ITIMER_REAL, timeout)
        return timeit.timeit(lambda: fn(data), number=1)
    except TimeoutError:
        return f"> {timeout:g} с"
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)


def bench_sorts(n, timeout):
    data = [random.randint(-n, n) for _ in range(n)]
    rows = []

    seconds = timeit.timeit(lambda: sorted(data), number=10) / 10
    rows.append(("sort", n, "sorted", seconds))

    for fn in (bubble_sort, insertion_sort, selection_sort):
        if n >= 100_000:
            seconds = measure_sort(fn, data, timeout)
        else:
            seconds = timeit.timeit(lambda: fn(data), number=1)
        rows.append(("sort", n, fn.__name__, seconds))

    return rows


def bench_search(n=SEARCH_SIZE, queries_count=SEARCH_QUERIES):
    data = [random.randint(-n, n) for _ in range(n)]
    queries = [random.randint(-n, n) for _ in range(queries_count)]

    seconds = timeit.timeit(lambda: sorted(data), number=10) / 10
    rows = [("search_prepare", n, "sorted", seconds)]
    ordered = sorted(data)

    def run_linear():
        for x in queries:
            linear_search(data, x)

    def run_binary():
        for x in queries:
            binary_search(ordered, x)

    rows.append(("search", n, "linear_search", timeit.timeit(run_linear, number=1)))
    rows.append(("search", n, "binary_search", timeit.timeit(run_binary, number=1)))
    return rows


def bench_two_sum(n):
    if n < 2:
        raise ValueError("Для Two Sum нужны хотя бы два элемента")

    data = [random.randint(1, 10 * n) for _ in range(n)]
    data[-2:] = [-1, -2]
    target = -3
    rows = []

    for fn in (two_sum_brute, two_sum_fast):
        seconds = timeit.timeit(lambda: fn(data, target), number=1)
        rows.append(("two_sum", n, fn.__name__, seconds))

    return rows

#=============================================================================

def print_rows(rows):
    for task, n, impl, seconds in rows:
        value = seconds if isinstance(seconds, str) else f"{seconds:.6f}"
        print(f"{task:<16} {n:>9} {impl:<20} {value:>14}", flush=True)

#==================================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="Бенчмарк поиска и сортировок ЛР7")
    parser.add_argument('--out', dest='out', required=True, help='Путь к отчётному файлу')
    parser.add_argument('--timeout', dest='timeout', type=float, default=60.0, help='Время обрыва функций')
    args = parser.parse_args()
    if not isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout должен быть положительным конечным числом")
    OUTPUT_PATH = Path(args.out)
    random.seed(42)
    rows = []
    print("seconds — время одного запуска; для поиска — всех запросов.")
    print(f"Свои сортировки при n >= 100 000 ограничены {args.timeout} секундами каждая.")
    print(f"{HEADER[0]:<16} {HEADER[1]:>9} {HEADER[2]:<20} {HEADER[3]:>14}")

    for n in SORT_SIZES:
        print(f"\nСортировки: n={n}", flush=True)
        measured = bench_sorts(n, args.timeout)
        rows.extend(measured)
        print_rows(measured)
        write_csv(rows, OUTPUT_PATH, header=HEADER)

    print(f"\nПоиск: n={SEARCH_SIZE}, запросов={SEARCH_QUERIES}", flush=True)
    measured = bench_search()
    rows.extend(measured)
    print_rows(measured)
    write_csv(rows, OUTPUT_PATH, header=HEADER)

    for n in TWO_SUM_SIZES:
        print(f"\nTwo Sum: n={n}, target=-3, пара в конце списка", flush=True)
        measured = bench_two_sum(n)
        rows.extend(measured)
        print_rows(measured)
        write_csv(rows, OUTPUT_PATH, header=HEADER)

    print(f"\nРезультаты сохранены: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
