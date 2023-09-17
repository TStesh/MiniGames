from itertools import *
from copy import deepcopy


# Инициализация
def init(l):
    s = [[] * 9 for i in range(9)]
    for i, v in enumerate(l):
        if i > 8:
            break
        if len(v) != 9:
            print(f'Некорректная строка = {v}')
            return 0
        s[i] = list(map(lambda x: int(x), list(v)))
    if i < 8:
        print(f'Количество строк = {i}')
        return 0
    return s


# Список пар индексов нулевых элементов
ip = lambda l: list(filter(lambda x: not l[x[0]][x[1]], product(range(9), repeat=2)))


# Список цифр, которые можно подставить
def dg(s, q):
    i, j = q
    n = list(filter(None, s[i][:j])) + list(filter(None, s[i][j + 1:]))
    n += [s[k][j] for k in range(9) if k != i and s[k][j]]
    m = map(lambda x: (x[0] + 3 * (i // 3), x[1] + 3 * (j // 3)), product(range(3), repeat=2))
    f = filter(lambda y: (y[0] != i or y[1] != j) and s[y[0]][y[1]], m)
    n += [s[z[0]][z[1]] for z in f]
    return list(filter(lambda x: x not in n, range(1, 10)))


# Гарантированное заполнение нулевых элементов
# Этой функции достаточно для простых судоку
def fn(s, p):
    while 1:
        for q in p:
            v = dg(s, q)
            if len(v) == 1:
                s[q[0]][q[1]] = v[0]
        p_new = ip(s)
        cp = len(p_new)
        if not cp:
            return s, True
        if cp == len(p):
            return s, False
        p = p_new


# Возращаем элемент с минимальным количеством подставляемых цифр
def me(s, p):
    l = list(map(lambda x: (x, len(dg(s, x))), p))
    return (next(filter(lambda x: x[1] == min(x[1] for x in l), l)))[0]


# Генерация разных вариантов заполнения пустых элементов
# Эта функция работает на сложных судоку
def fd(s, p, m=0, d=[]):
    if len(d) > 1_000_000 or not len(p):
        return s, False
    q = me(s, p)
    p.remove(q)
    i, j = q
    if not m:
        for v in dg(s, q):
            d.insert(0, deepcopy(s))
            d[0][i][j] = v
    else:
        x = []
        for s in d:
            vl = dg(s, q)
            if vl:
                for v in vl:
                    x.insert(0, deepcopy(s))
                    x[0][i][j] = v
                    r = fn(x[0], p)
                    if r[1]:
                        return r[0], True
        if x:
            d += x
            print(f'Глубина рекурсии = {m}, количество вариантов = {len(d)}')
    return fd(s, p, m + 1, d)


# Генерация разных вариантов заполнения пустых элементов
# Эта функция работает на сложных судоку
# Возможность добавить начальный нулевой элемент
def fd2(s, p, m=0, d=[], h=None):
    if len(d) > 5_000:
        return s, False
    q = deepcopy(h) if h else me(s, p)
    p.remove(q)
    i, j = q
    if not m:
        for v in dg(s, q):
            d.insert(0, deepcopy(s))
            d[0][i][j] = v
    else:
        x = []
        for s in d:
            vl = dg(s, q)
            if vl:
                for v in vl:
                    x.insert(0, deepcopy(s))
                    x[0][i][j] = v
                    r = fn(x[0], p)
                    if r[1]:
                        return r[0], True
        if x:
            d += x
            # print(f'Глубина рекурсии = {m}, количество вариантов = {len(d)}')
    return fd2(s, p, m + 1, d)


# Главная функция
def main(s):
    r = fn(s, ip(s))
    if r[1]:
        return r[0]
    else:
        l = list(map(lambda x: (x, len(dg(r[0], x))), ip(r[0])))
        if len(l) == 1:
            r = fd(r[0], ip(r[0]))
            return r[0] if r[1] else False
        for a in list(filter(lambda x: x[1] == min(x[1] for x in l), l)):
            u = fd2(r[0], ip(r[0]), h=a[0])
            if u[1]:
                return u[0]
        r = fd(r[0], ip(r[0]))
        return r[0] if r[1] else False


f = open('sudoku.txt', 'r')
l = [line.strip() for line in f]
f.close()
sd = init(l)
if not sd:
    print('Некорректный формат судоку')
else:
    r = fn(sd, ip(sd))
    if r[1]:
        print('1-решение:', r[0])
    else:
        l = list(map(lambda x: (x, len(dg(r[0], x))), ip(r[0])))
        if len(l) == 1:
            print('Запуск полной рекурсии:')
            r = fd(r[0], ip(r[0]))
            if r[1]:
                print('2-решение:', r[0])
            else:
                print('Решить не удалось')
        is_slv = False
        for a in list(filter(lambda x: x[1] == min(x[1] for x in l), l)):
            print(f'Пробуем элемент:', a[0])
            u = fd2(r[0], ip(r[0]), h=a[0])
            if u[1]:
                is_slv = True
                print('3-решение:', u[0])
                break
        if not is_slv:
            print('\nЗапуск полной рекурсии:')
            r = fd(r[0], ip(r[0]))
            if r[1]:
                print('2-решение:', r[0])
            else:
                print('Решить не удалось')