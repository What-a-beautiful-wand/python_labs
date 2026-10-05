import csv
from pathlib import Path
from typing import Iterable, Sequence

def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    p = Path(path)
    return p.read_text(encoding=encoding)

#=======================================================================

def ensure_parent_dir(path: str | Path) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

#=======================================================================

def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:    
    rows = list(rows)

    if not rows and header is None:
        raise ValueError('rows не может быть пустым')

    standart_len = len(rows[0]) if header is None else len(header)
    for row in rows:
        if len(row) != standart_len:
            raise ValueError('Все строки должны быть одинаковой длинны')

    ensure_parent_dir(path=path)
    p = Path(path)


    with p.open("w", newline="", encoding="utf-8") as file:
        w = csv.writer(file)
        if header is not None:
            w.writerow(header)

        for r in rows:
            w.writerow(r)