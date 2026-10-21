import argparse
import csv
import sys
from pathlib import Path

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.lib.text import normalize, tokenize, count_freq, top_n
from src.lib.text_stats import text_statistic
from src.lab04.io_txt_csv import read_text, write_csv

def frequencies_from_text(text: str) -> dict[str, int]:
    """Нормализовать текст и посчитать частоты слов."""
    tokens = tokenize(normalize(text))
    return count_freq(tokens)

#=======================================================================

def sorted_word_counts(freq: dict[str, int]) -> list[tuple[str, int]]:
    """Отсортировать слова по убыванию частоты, затем по алфавиту."""
    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))

#=======================================================================

def main() -> int:
    """Прочитать файлы, записать отчёты и вывести статистику."""
    parser = argparse.ArgumentParser(description='Отчёт по частотам слов')
    parser.add_argument('--in', dest='inputs', nargs='+',
                        default=['data/lab04/input.txt'], help='Входные TXT-файлы')
    parser.add_argument('--out', help='Путь к отчёту word,count')
    parser.add_argument('--encoding', default='utf-8', help='Кодировка входных файлов')
    parser.add_argument('--per-file', help='Путь к отчёту file,word,count')
    parser.add_argument('--total', help='Путь к сводному отчёту word,count')
    parser.add_argument('--table', action='store_true', help='Вывести таблицу частот')
    args = parser.parse_args()

    try:
        texts = []
        per_file = []
        for path in sorted(set(args.inputs)):
            text = read_text(path, encoding=args.encoding)
            texts.append(text)
            counts = frequencies_from_text(text)

            for word, count in sorted_word_counts(counts):
                per_file.append((str(Path(path)), word, count))

        per_file.sort(key=lambda x: (x[0], -x[2], x[1]))
        text = '\n'.join(texts)
        counts = frequencies_from_text(text)
        rows = sorted_word_counts(counts)

        if len(args.inputs) > 1 or args.per_file is not None:
            path = args.per_file or 'data/lab04/report_per_file.csv'
            write_csv(per_file, path, header=('file', 'word', 'count'))
            path = args.total or args.out or 'data/lab04/report_total.csv'
        else:
            path = args.total or args.out or 'data/lab04/report.csv'

        write_csv(rows, path, header=('word', 'count'))
        if args.out is not None and args.total is not None and args.out != args.total:
            write_csv(rows, args.out, header=('word', 'count'))

        print(f'Всего слов: {sum(counts.values())}')
        print(f'Уникальных слов: {len(counts)}')
        print('Топ-5:')
        for word, count in top_n(counts, n=5):
            print(f'{word}:{count}')

        if args.table:
            print(text_statistic(text, table_form=True))

    except FileNotFoundError as error:
        print(f'Ошибка: файл не найден: {error.filename}', file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print('Ошибка: не удалось прочитать текст. Проверьте --encoding (например, cp1251).',
              file=sys.stderr)
        return 1
    except LookupError:
        print(f'Ошибка: неизвестная кодировка: {args.encoding}', file=sys.stderr)
        return 1
    except (OSError, ValueError, csv.Error) as error:
        print(f'Ошибка при создании отчёта: {error}', file=sys.stderr)
        return 1

    return 0

#=======================================================================

if __name__ == '__main__':
    sys.exit(main())
