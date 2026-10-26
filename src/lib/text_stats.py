import sys
from pathlib import Path

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.lib.text import normalize, tokenize, count_freq, top_n

def text_statistic(text: str, n: int = 3, table_form: bool = False) -> str:
    normal_text = normalize(text)
    tokens = tokenize(normal_text)
    counts = count_freq(tokens)

    if n > len(counts.keys()):
        n = len(counts.keys())

    top = top_n(freq=counts, n=n)

    if table_form:
        table = []
        max_len = max([len('Слово')] + [len(word) for word in counts]) + 5
        max_num_len = max([len('Частота')] + [len(str(count)) for count in counts.values()]) + 2

        table.append('+' + '-' * (max_len) + '+' + '-' * (max_num_len) + '+')
        table.append(f'|{"Слово":<{max_len}}|{"Частота":>{max_num_len}}|')
        table.append('+' + '-' * (max_len) + '+' + '-' * (max_num_len) + '+')

        for word, count in top_n(counts, n=n):
            table.append(f'|{word:<{max_len}}|{count:>{max_num_len}}|')

        table.append('+' + '-' * (max_len) + '+' + '-' * (max_num_len) + '+')
        
        return '\n'.join(table)

    else:
        top_text = "\n".join(
            f"{word}: {count}"
            for word, count in top
        )

        return (
            f"Всего слов: {len(tokens)}\n"
            f"Уникальных слов: {len(counts)}\n"
            f"Топ слов:\n{top_text}"
        )

if __name__ == '__main__':
    print('Введите что-то:', end='\n')
    text = sys.stdin.read()

    print(text_statistic(text, table_form=True, n=100))
