import re

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:

    if not text: return text

    if casefold: text = text.casefold()

    if yo2e: text = text.replace('ё', 'е').replace('Ё', 'Е')

    text = text.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    return ' '.join(text.split())

#==========================================================================

def tokenize(text: str) -> list[str]: return re.findall(r'\w+(?:-\w+)*', text)

#===========================================================================

def count_freq(tokens: list[str]) -> dict[str, int]:

    result = {}

    for token in tokens:
        try:
            result[token] += 1
        except KeyError:
            result.update({token:1})

    return result

#============================================================================

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    if n < 0:
        raise ValueError("n не может быть отрицательным")

    return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:n]