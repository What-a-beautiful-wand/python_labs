from text import *

def text_statistic(text: str) -> str:
    normal_text = normalize(text)
    tokens = tokenize(normal_text)
    counts = count_freq(tokens)
    top = top_n(counts)

    top_text = "\n".join(
        f"{word}: {count}"
        for word, count in top
    )

    return (
        f"Всего слов: {len(tokens)}\n"
        f"Уникальных слов: {len(counts)}\n"
        f"Топ слов:\n{top_text}"
    )

print(text_statistic("Привет, мир! Привет!!!"))