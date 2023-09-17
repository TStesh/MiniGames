from copy import deepcopy

N = 9
NN = N * (N + 1) // 2

sudoku = [
    '35:1,1,1,2,2,1,3,1,4,1,4,2,5,1',
    '27:1,3,2,2,2,3,3,2,3,3',
    '31:1,4,1,5,2,4,2,5,2,6,3,5',
    '14:1,6,1,7,1,8',
    '21:1,9,2,7,2,8,2,9,3,7',
    '17:3,8,3,9',
    '17:3,4,4,3,4,4',
    '4:3,6,4,6',
    '12:5,2,6,1,6,2,6,3',
    '17:5,3,5,4',
    '8:4,5,5,5,6,5',
    '7:5,6,5,7',
    '22:4,7,4,8,4,9,5,8',
    '38:5,9,6,8,6,9,7,9,8,9,9,8,9,9',
    '10:6,4,7,4',
    '20:6,6,6,7,7,6',
    '6:7,1,7,2',
    '34:7,3,8,1,8,2,8,3,9,1',
    '10:9,2,9,3,9,4',
    '29:7,5,8,4,8,5,8,6,9,5,9,6',
    '26:7,7,7,8,8,7,8,8,9,7'
]


def print_table(t):
    m = len(str(max(max(t))))
    fm = '{0:' + str(m) + '} '
    fv = '-' * (m + 1)
    for i, line in enumerate(t):
        s, v, k = '', '', 1
        for _ in line:
            s += fm.format(_)
            v += fv
            if not k % 3 and k < N - 1:
                s += '| '
                v += '+-'
            k += 1
        print(s)
        if not (i + 1) % 3 and i < N - 1:
            print(v[:-1])


def check_input_data():
    d = [[0] * N for i in range(N)]
    sd = [[0] * N for i in range(N)]
    ss = {}
    for s in sudoku:
        cells_sum, cells = s.split(':')
        cells_pos = cells.split(',')
        pos_x = [int(v) - 1 for k, v in enumerate(cells_pos) if not k % 2]
        pos_y = [int(v) - 1 for k, v in enumerate(cells_pos) if k % 2]
        lx, ly = len(pos_x), len(pos_y)
        if lx != ly:
            return 1, []
        cells_sum = int(cells_sum + '0')
        while cells_sum in ss:
            cells_sum += 1
        ss[cells_sum] = 0
        for k in range(lx):
            d[pos_x[k]][pos_y[k]] += 1
            sd[pos_x[k]][pos_y[k]] = cells_sum
    l0 = [(i, j) for i in range(N) for j in range(N) if d[i][j] == 0]
    if l0:
        return 2, l0
    l1 = [(i, j) for i in range(N) for j in range(N) if d[i][j] > 1]
    if l1:
        return 3, l1
    return 0, sd


def check_lines(t):
    d = [[0] * N for i in range(N)]
    for i, line in enumerate(t):
        a = set(line)
        b = set(t[i + 1]) if i < N - 1 else set(t[-2])
        z = a.intersection(b)
        if len(z) == 1:
            print(z)


# cумма сумм ячеек клетки
def sum_big_cells(t, i, j):
    p, q = 1, 1j
    z = {t[i][j]}
    for _ in range(4):
        x, y = int(p.real), int(p.imag)
        for k in range(3):
            z.add(t[i + x][j + k - 1]) if x else z.add(t[i + k - 1][j + y])
        p *= q
    s = sum([_ // 10 for _ in z])
    return s


def check_big_cells(t):
    d = [[0] * N for i in range(N)]
    for i in range(1, N, 3):
        for j in range(1, N, 3):
            v, w = [], []
            # обход ребер квадрата с внутренней стороны:
            # (i,j) - центральная клетка
            # Верх: (-1, 0) Низ: (1, 0) Левый: (0, -1) Правый: (0, 1)
            p, q = 1, 1j
            for _ in range(4):
                x, y = int(p.real), int(p.imag)
                if x:
                    m = 2 * x
                    if 0 <= i + m < N:
                        for k in range(3):
                            ind_x, ind_y = i + m, j + k - 1
                            g, h = t[i + x][ind_y], t[ind_x][ind_y]
                            if g == h:
                                if g != t[ind_x + x][ind_y]:
                                    v.append((ind_x, ind_y))
                                if g != t[i][ind_y]:
                                    w.append((i + x, ind_y))
                else:
                    m = 2 * y
                    if 0 <= j + m < N:
                        for k in range(3):
                            ind_x, ind_y = i + k - 1, j + m
                            g, h = t[ind_x][j + y], t[ind_x][ind_y]
                            if g == h:
                                if g != t[ind_x][ind_y + y]:
                                    v.append((ind_x, ind_y))
                                if g != t[ind_x][j]:
                                    w.append((ind_x, j + y))
                p *= q
            if len(v) == 1 and not w:
                d[v[0][0]][v[0][1]] = sum_big_cells(t, i, j) - NN
            if len(w) == 1 and not v:
                st = t[v[0][0]][v[0][1]] // 10
                d[v[0][0]][v[0][1]] = NN - sum_big_cells(t, i, j) + st
    return d


def num_split(n, m, d=[]):
    if m == 1:
        if 1 <= n <= 9:
            d.append(n)
            print(d)
            return d
        else:
            return False
    else:
        fr = d[-1] + 1 if d else 1
        to = (n - m * (m - 1) // 2) // m
        for _ in range(fr, to + 1):
            wd = deepcopy(d)
            wd.append(_)
            num_split(n - _, m - 1, wd)


def start():
    code, t = check_input_data()
    if code:
        print('Ошибка с кодом', code, ':', t)
        return False
    check_lines(t)
    d = check_big_cells(t)
    print_table(d)


start()
