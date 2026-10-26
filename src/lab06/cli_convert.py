import argparse
from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx

def main() -> None:
    parser = argparse.ArgumentParser(description="Конвертеры данных")
    sub = parser.add_subparsers(dest="cmd")

    pJ2C = sub.add_parser("json2csv")
    pJ2C.add_argument("--in", dest="input", required=True)
    pJ2C.add_argument("--out", dest="output", required=True)

    pC2J = sub.add_parser("csv2json")
    pC2J.add_argument("--in", dest="input", required=True)
    pC2J.add_argument("--out", dest="output", required=True)

    pC2X = sub.add_parser("csv2xlsx")
    pC2X.add_argument("--in", dest="input", required=True)
    pC2X.add_argument("--out", dest="output", required=True)

    args = parser.parse_args()

    if args.cmd == "json2csv":
        json_to_csv(args.input, args.output)

    elif args.cmd == "csv2json":
        csv_to_json(args.input, args.output)

    elif args.cmd == "csv2xlsx":
        csv_to_xlsx(args.input, args.output)

if __name__ == '__main__':
    main()