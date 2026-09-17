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

def col_sums(mat: list[list[float | int]]) -> list[float]:
    mat = transpose(mat)
    return row_sums(mat)