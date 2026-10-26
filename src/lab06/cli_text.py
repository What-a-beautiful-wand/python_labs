import argparse
from pathlib import Path
from src.lib.text_stats import text_statistic

def main() -> None:
    parser = argparse.ArgumentParser(description="CLI‑утилиты лабораторной №6")
    subparsers = parser.add_subparsers(dest="command")

    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла")
    cat_parser.add_argument("--input", dest="input", required=True)
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки")

    stats_parser = subparsers.add_parser("stats", help="Частоты слов")
    stats_parser.add_argument("--input", dest="input", required=True)
    stats_parser.add_argument("--table", dest="table_form", action="store_true")
    stats_parser.add_argument("--top", dest="top", type=int, default=5)

    args = parser.parse_args()

    if args.command == "cat":
        path = Path(args.input)

        with path.open(encoding="utf-8") as file:
            for number, line in enumerate(file, start=1):
                if args.n:
                    print(f"{number}: {line}", end="")
                else:
                    print(line, end="")
            
    elif args.command == "stats":
        path = Path(args.input)

        with path.open(encoding='utf-8') as file:
            text = file.read()

        print(text_statistic(text=text, n=args.top, table_form=args.table_form))

if __name__ == '__main__':
    main()
