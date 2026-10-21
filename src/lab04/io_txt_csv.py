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
    """Записать CSV в UTF-8. Разная длина строк приводит к ValueError."""
    rows = list(rows)

    check_rows = rows if header is None else [header] + rows
    for column in zip(*check_rows, strict=True):
        pass

    ensure_parent_dir(path=path)
    p = Path(path)


    with p.open("w", newline="", encoding="utf-8") as file:
        w = csv.writer(file)
        if header is not None:
            w.writerow(header)

        for r in rows:
            w.writerow(r)
