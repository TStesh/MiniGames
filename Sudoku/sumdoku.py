DIM_BLOCK, DIM_TBL, MAGIC = 3, 9, 100

cell_sum_groups = (

)

filled_cells = []


# Функция возвращает координаты ячейки по ее номеру
def n2c(cell_num):
    x, y = divmod(cell_num - 1, DIM_TBL)
    return x, y


# Функция генерации таблицы по списку заполненных ячеек
# @f_cells - список заполненных ячеек
def lst2tbl(f_cells):
    tbl = [[0] * DIM_TBL for _ in range(DIM_TBL)]
    for cell in f_cells:
        d, cell_num = cell
        cell_x, cell_y = n2c(cell_num)
        tbl[cell_x][cell_y] = d
    return tbl


# Функция проверяет возможность размещения в заданной ячейке заданной цифры
# @f_cells - список заполненных ячеек, @row - строка, @col - столбец, @digit - цифра
def check_val(f_cells, row, col, digit):
    tbl = lst2tbl(f_cells)
    if digit in tbl[row]:
        return False
    if digit in [tbl[i][col] for i in range(DIM_TBL)]:
        return False
    sx, sy = DIM_BLOCK * (row // DIM_BLOCK), DIM_BLOCK * (col // DIM_BLOCK)
    block = [tbl[sx + i][sy + j] for i in range(DIM_BLOCK) for j in range(DIM_BLOCK)]
    if digit in block:
        return False
    return True


# Функция вычисляет список подходящих цифр для заданной ячейки
# @f_cells - список заполненных ячеек, @cell_num - номер ячейки
def suit_digits(f_cells, cell_num):
    suit_d = []
    r, c = n2c(cell_num)
    for x in range(1, DIM_TBL + 1):
        if check_val(f_cells, r, c, x):
            suit_d.append(x)
    return suit_d


# Функция генерирует список пустых ячеек
# @f_cells - список заполненных ячеек
def empty_cells(f_cells):
    not_empty_cells = []
    for cell in f_cells:
        _, cell_num = cell
        not_empty_cells.append(cell_num)
    e_cells = [x for x in range(DIM_TBL ** 2) if x not in not_empty_cells]
    return e_cells


# Функция определения ячеек с наименьшим количеством подходящим цифр
# @f_cells - список заполненных ячеек
def suit_cells(f_cells):
    e_cells = empty_cells(f_cells)
    min_len_s = MAGIC
    for cell in e_cells:
        len_s = len(suit_digits(f_cells, cell))
        if min_len_s > len_s:
            min_len_s = len_s
    s_sells = []
    if min_len_s > 0:
        for cell in e_cells:
            s_digs = suit_digits(f_cells, cell)
            if len(s_digs) == min_len_s:
                s_sells.append(cell)
    return min_len_s, s_sells


# Функция генерации списка разбиений числа на заданное число слагаемых, каждое из которых не превышает 9
# @num - заданное число, @qty - заданное число слагаемых, @r - массив разбиений (при первом вызове пустой)
# example: rns(38, 7, [])
def rns(num, qty, r, k=0):
    if k == 0:
        for x in range(1, num // qty - (qty - 1) // 2 + 1):
            r.append([x])
        return rns(num, qty, r, k + 1)
    if k == qty:
        r1 = []
        for x in r:
            if sum(x) == num:
                r1.append(x[:])
        return r1
    r1 = []
    s = 0
    for x in r:
        for y in range(x[k - 1] + 1, DIM_TBL + 1):
            if sum(x) + y <= num:
                r1.append(x[:])
                r1[s].append(y)
                s += 1
    return rns(num, qty, r1, k + 1)


# Функция для определения группы с наименьшим числом разбиений
def gen_pair_list(f_cells):
    pair_list, min_split_num = [], MAGIC
    for idx, group in enumerate(cell_sum_groups):
        num, pos_list = group
        pos_list_len = len(pos_list)
        for cell in f_cells:
            d, pos = cell
            if pos in pos_list:
                num -= d
                pos_list_len -= 1
                break
        if pos_list_len > 1:
            split_list = rns(num, pos_list_len, [])
            split_num = len(split_list)
            if split_num < min_split_num:
                min_split_num = split_num
            pair_list.append((idx, num, pos_list_len, split_num))
        else:
            pair_list.append((idx, num, 1, 1))
            min_split_num = 1
    suit_pair_list = []
    for pair in pair_list:
        idx, *_, split_num = pair
        if split_num == min_split_num:
            suit_pair_list.append(idx)
    return min_split_num, suit_pair_list


# Функция


m_split_num, suit_indexes = gen_pair_list(filled_cells)


