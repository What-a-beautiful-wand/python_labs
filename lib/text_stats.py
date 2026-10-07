from text import *
import sys

def text_statistic(text: str, n: int = 3, table_form: bool = False) -> str:
    normal_text = normalize(text)
    tokens = tokenize(normal_text)
    counts = count_freq(tokens)

    if n > len(counts.keys()):
        n = len(counts.keys())

    top = top_n(freq=counts, n=n)

    if table_form:
        table = []
        max_len = max(len(max(tokens, key=len)), len('Слово')) + 5
        max_num_len = max(max(counts.values()), len('Частота')) + 2

        table.append('+' + '-' * (max_len) + '+' + '-' * (max_num_len) + '+')
        table.append(f'|{'Слово':<{max_len}}|{'Частота':>{max_num_len}}|')
        table.append('+' + '-' * (max_len) + '+' + '-' * (max_num_len) + '+')

        for word in counts.keys():
            count = counts[word]
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

print('Введите что-то:', end='\n')
text = sys.stdin.read()

print(text_statistic(text, table_form=True, n=100))