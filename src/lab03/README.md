# ЛАБОЛАТРНАЯ РАБОТА №3

## ЗАДАНИЕ 1

### ФУНКЦИЯ 1

   def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:

    if not text: return text

    if casefold: text = text.casefold()

    if yo2e: text = text.replace('ё', 'е').replace('Ё', 'Е')

    text = text.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    return ' '.join(text.split())
   
![Пример_работы_кода_1]()

Сзодаем функцию для нормализации кода. Сразу отбразываем пустую строку. Если casefold True тогда применяем функцию casefold() также если yo2e True заменяем ё->е и Ё->Е. Заменяем все специальные символы на пробел и удаляем все ненужные пробелы.

### ФУНКЦИЯ 2

   def tokenize(text: str) -> list[str]: return re.findall(r'\w+(?:-\w+)*', text)

![Пример_работы_кода_2]()

Через библиотеку re ищем все подстроки, удовлетворяющие '\w+(?:-\w+)*' и собираем их в список.

### ФУНКЦИЯ 3

   def count_freq(tokens: list[str]) -> dict[str, int]:

      result = {}

      for token in tokens:
         try:
            result[token] += 1
         except KeyError:
            result.update({token:1})

      return result

![Пример_работы_кода_3]()

Проходимся по каждому слову, пытаемся добавить его в словарь, если не получается, тогда добавляем это слово в словарь.

### ФУНКЦИЯ 4

   def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
      if n <= 0:
         raise ValueError("n не может быть отрицательным")

      return sorted(freq.items(), key=lambda x: (-x[1], x[0]))[:n]

![Пример_работы_кода_4]()

Проверяем, чтобы n было больше 0 и возвращаем отсорированный список по ключу (-x[1], [0]) и обрезаем его n

## ЗАДАНИЕ 2 + СО СВЁЗДОЧКОЙ

### БЕЗ ТАБЛИЦЫ

   def text_statistic(text: str, n: int = 3, table_form: bool = False) -> str:
    normal_text = normalize(text)
    tokens = tokenize(normal_text)
    counts = count_freq(tokens)
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

![Пример_работы_кода_5]()

Получаем на вход несколько строк, так как считываем все до конца файла. Получаем топ слов, преобразуем его в красивый вид и выводим.

### С ТАБЛИЦЕЙ

![Пример_работы_кода_6]()

Код такой же, но теперт если table_form True, то мы создаём таблицу, ищем максимальнцю длину каждого столбца, оформляем красивую таблицу и добавляем в неё слова форматируя их сдвигая влево и вправо на максимальное количевство символов.