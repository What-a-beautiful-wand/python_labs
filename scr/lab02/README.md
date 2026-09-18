# Лабораторная Работа №2

### Задание 1

#### Функция 1

    def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
        
        if not nums:
            raise ValueError('Пустой список не принимается')
        
        max_num, min_num = nums[0], nums[0]

        for number in nums:
            if max_num < number:
                max_num = number
            elif min_num > number:
                min_num = number

        return (min_num, max_num)

![Пример_работ_кода_1](https://github.com/What-a-beautiful-wand/python_labs/blob/main/img/lab02/ex01.png)

Принимаем на вход список, вызываем ошибку если он пустой, создаём примеры минимального и максимального чиса, проходимся по ссписку, сравнимваем попавшиеся числа и перезаписываем по нужде.

#### Функция 2

    def unique_sorted(nums: list[float | int]) -> list[float | int]:
        
        return sorted(list(set(nums)))

![Пример_работы_кода_2](https://github.com/What-a-beautiful-wand/python_labs/blob/main/img/lab02/ex02.png)

Принимаем на вход список, делаем из него множество, чтобы убрать повторяющиеся элементы, превращаем обратно в список, и снова сортируем, потому что множество отрицательные числа кидает в конец.

#### Функция 3

    def flatten(mat: list[list | tuple]) -> list:
        line = []
        for lst in mat:
            if lst.__class__ == list or lst.__class__ == tuple:
                line += lst
                
            else:
                raise TypeError('Такой тип недопустим')

        return line

![Пример_работы_кода_3](https://github.com/What-a-beautiful-wand/python_labs/blob/main/img/lab02/ex03.png)

Принимаем на вход список, состоящий из списков и картежей. Создаем новый список, в который запишем все числа из входящий в него чисел. Проходимся по вложенным спискам, и присоединяем их к новому, только если это картеж или список, всё остальное отлетает в ошибку.

===============================================================================

### Задание 2

#### Функция 1

    def transpose(mat: list[list[float | int]]) -> list[list]:
        
        if not mat:
            return mat

        m = len(mat)
        n = len(mat[0])


        for line in mat:
            if n != len(line):
                raise ValueError('Это не матрица')

        new_mat = [[0] * m for _ in range(n)]

        for line_index in range(m):
            for column_index in range(n):
                new_mat[column_index][line_index] = mat[line_index][column_index]

        return new_mat

![4](https://github.com/What-a-beautiful-wand/python_labs/blob/main/img/lab02/ex04.png)

Принимаем матрицу на вход, тутже возвращаем ее если она пустая, смотрим её размеры и проверяем, чтобы матрица была не "рваная". Создаём новую матрицу с новой размерностью. проходимся по всем индексам строк и столбцов. В новую матрицу записываем их меняя месстами.

#### Функция 2

    def row_sums(mat: list[list[float | int]]) -> list[float]:
        
        if not mat:
            return mat
        
        m = len(mat)
        n = len(mat[0])

        for line in mat:
            if n != len(line):
                raise ValueError('Это не матрица')

        sums = []

        for line in mat:
            sums.append(sum(line))

        return sums

![5](https://github.com/What-a-beautiful-wand/python_labs/blob/main/img/lab02/ex05.png)

Принимаем на вход матрицу, если она пустая возвращаем её же. Проверяем чтобы она была не рваная. Проходимся по всем строкам, к котоорым применяем функцию sum и добавляя её в список всех сумм.

#### Функция 6

    def col_sums(mat: list[list[float | int]]) -> list[float]:
        
        mat = transpose(mat)
        return row_sums(mat)

![6](https://github.com/What-a-beautiful-wand/python_labs/blob/main/img/lab02/ex06.png)

Транспонируем полученную матрицу и применяем к ней сумму по строкам, так получаем сумму по столбцам исходной матрицы.

=============================================================================

### Задание 3

    def format_record(rec: tuple[str, str, float]) -> str:

        name = rec[0]
        group = rec[1]
        gpa = rec[2]

        if not name or not group or not gpa:
            raise ValueError('Поля не должны быть пустыми')

        if name.__class__ != str:
            raise TypeError('Имя должно быть строкой')
        if group.__class__ != str:
            raise TypeError('Группа должна быть строкой')
        if gpa.__class__ != float and gpa.__class__ != int:
            raise TypeError('GPA должно быть числом')

        name = rec[0].title().split()

        try:
            name = f'{name[0]} {name[1][0]}.{name[2][0]}.'
        except IndexError:
            name = f'{name[0]} {name[1][0]}.'

        gpa = f'{round(gpa, 2):.2f}'

        return f'{name}, гр. {group}, GPA {gpa}'

![7](https://github.com/What-a-beautiful-wand/python_labs/blob/main/img/lab02/ex07.png)

Получаем на вход картеж из данных, проверяем чтобы все они правильного типа и не пустые, инчае кидаем ошибку. Преобоазуем каждую первую букву строки в большую и делим её split на подстроки. Пытаемся перезаписать в имя ФИО, если не получается, значит есть только фамилия и имя. Округляем GPA до двух знаков после запятой и выводим всё.