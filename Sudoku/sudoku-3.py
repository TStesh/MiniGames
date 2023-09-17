# Классичесий судоку
# с допусловием что на главных диагоналях стоят разные числа
from copy import deepcopy

SSIZE = 3
TSIZE = SSIZE ** 2


class Table:
    def __init__(self, tbl):
        self.tbl = deepcopy(tbl)

    def null_cells(self):
        null_cells = []
        for i in range(TSIZE):
            for j in range(TSIZE):
                if self.tbl[i][j] == 0:
                    null_cells.append((i, j))
        return null_cells

    def suit_digits(self, row, col):
        suit_d = []
        if self.tbl[row][col]:
            return suit_d
        all_digits = [_ for _ in range(1, TSIZE + 1)]
        for digit in all_digits:
            if digit in self.tbl[row]:
                continue
            is_continue = True
            for _ in range(TSIZE):
                if digit == self.tbl[_][col]:
                    is_continue = False
                    break
            if is_continue:
                start_row, start_col = row - row % SSIZE, col - col % SSIZE
                for i in range(SSIZE):
                    for j in range(SSIZE):
                        if self.tbl[start_row + i][start_col + j] == digit:
                            is_continue = False
                            break
                    if not is_continue:
                        break
            if is_continue:
                suit_d.append(digit)
        return suit_d

    def start_cell(self):
        min_len_d, suit_row, suit_column = TSIZE, -1, -1
        null_p = self.null_cells()
        for null_c in null_p:
            x, y = null_c
            len_d = len(self.suit_digits(x, y))
            if len_d < min_len_d:
                min_len_d, suit_row, suit_column = len_d, x, y
        return suit_row, suit_column

    def check_diag(self):
        d, d1, d2 = [], [], []
        for i in range(TSIZE):
            d.append(i + 1)
            d1.append(self.tbl[TSIZE - i - 1][i])
            d2.append(self.tbl[i][i])
        return sorted(d1) == sorted(d2) == d

    def tbl_print(self):
        for i in range(TSIZE):
            for j in range(TSIZE):
                print(self.tbl[i][j], sep=',', end='')
            print()


class Sudoku:
    def __init__(self):
        sudoku_file = open('sudoku.txt', 'r')
        lines = [line.strip() for line in sudoku_file if line.strip()]
        sudoku_file.close()
        self.tbl = []
        for line in lines:
            self.tbl.append(list(map(lambda x: int(x), list(line))))
        # валидация
        self.bad_tbl = False
        for _ in range(TSIZE):
            if not self.check_row(_):
                self.bad_tbl = True
                break
        if not self.bad_tbl:
            for _ in range(TSIZE):
                if not self.check_column(_):
                    self.bad_tbl = True
                    break
        if not self.bad_tbl:
            for i in range(0, TSIZE, SSIZE):
                for j in range(0, TSIZE, SSIZE):
                    if not self.check_block(i, j):
                        self.bad_tbl = True
                        break
        if not self.bad_tbl:
            self.tables = [Table(self.tbl)]

    def check_row(self, row):
        line = [x for x in self.tbl[row] if x > 0]
        line_set = set(line)
        return len(line) == len(line_set)

    def check_column(self, column):
        line = []
        for _ in range(TSIZE):
            if self.tbl[_][column] > 0:
                line.append(self.tbl[_][column])
        line_set = set(line)
        return len(line) == len(line_set)

    def check_block(self, start_row, start_column):
        line = []
        for i in range(SSIZE):
            for j in range(SSIZE):
                if self.tbl[start_row + i][start_column + j] > 0:
                    line.append(self.tbl[start_row + i][start_column + j])
        line_set = set(line)
        return len(line) == len(line_set)

    def gen_tables(self):
        copy_tables = []
        for table in self.tables:
            null_p = table.null_cells()
            if not null_p:
                if table.check_diag():
                    print('Решение:')
                    table.tbl_print()
                    return False
                continue
            x, y = table.start_cell()
            suit_d = table.suit_digits(x, y)
            ds = len(suit_d)
            if not ds:
                continue
            # Если одна подходящая цифра, то идем максимально глубоко
            t = False
            cp_table = deepcopy(table)
            cp_table.tbl[x][y] = suit_d[0]
            while ds == 1:
                null_c = cp_table.null_cells()
                if not null_c:
                    if cp_table.check_diag():
                        print('Решение:')
                        cp_table.tbl_print()
                        return False
                    t = True
                    break
                x, y = cp_table.start_cell()
                suit_n = cp_table.suit_digits(x, y)
                ds = len(suit_n)
                if ds == 0:
                    t = True
                    break
                if ds > 1:
                    self.tables.append(cp_table)
                    t = True
                    break
                cp_table.tbl[x][y] = suit_n[0]
            if t:
                continue
            for d in suit_d:
                w_tbl = Table(table.tbl)
                w_tbl.tbl[x][y] = d
                copy_tables.append(w_tbl)
        self.tables = deepcopy(copy_tables)
        return True


sud = Sudoku()

if sud.bad_tbl:
    print('Invalid sudoku table')
else:
    counter = 1
    while sud.gen_tables() or len(sud.tables):
        print('Step = ', counter, ', Tables: ', len(sud.tables))
        counter += 1
    print('Total steps:', counter)
