"""
Морской бой

Правила игры:
Играют два игрока. У каждого сетка 10х10
В сетке расставляются корабли: 4 однопалубных, 3 двухпалубных, 2 трехпалубных и 1 четырехпалубный
Корабли не соприкасаются друг с другом, то есть соседние ячейки вокруг корабля должны быть пустыми.
Ход: игрок называет координаты ячейки. Если попадает в корабль противника, то делает следующий ход.
Если не попадает, ход переходит к противнику. Выигрывает тот, кто быстрее потопит все корабли.
"""
from random import choice


class Ship:

    def __init__(self, length: int, d: str, row: int, col: int):
        self.start_r, self.start_c = row, col
        self.direct, self.length = d, length
        self.state = [1] * length
        self.neighbour_cells = []

    def hit(self, r: int, c: int):
        ind = r - self.start_r if self.direct == 'V' else c - self.start_c
        print('State before:', self.state)
        self.state[ind] = 2
        print('State after:', self.state)

    # Если вернет 1, то корабль целый,
    # Если вернет 2, то корабль утопленный,
    # Если возвращает число между 1 и 2, то корабль подбит
    def get_state(self) -> float:
        return sum(self.state) / self.length


class Board:

    def __init__(self, size: int, ship_types: int):
        # чтобы не заморачиваться с проверкой размещения на границах,
        # добавим фиктивные колонки справа, слева, а также фиктивные строки сверху и снизу,
        # игровое поле будем начинать с (1, 1) и заканчивать (size + 1, size + 1)
        self.brd_size = size
        self.all_size = size + 2
        self.ship_types = ship_types
        # Игровая доска
        self.brd = [[0] * self.all_size for _ in range(self.all_size)]
        # Список кораблей на доске
        self.ships = []
        # Для быстрого определения корабля по позиции добавим словарь,
        # в котором ключом является позиция в доске, значением - индекс
        # в списке кораблей на доске
        self.ships_map = {}
        # Размещаем корабли
        self.place_ships(100)

    # Проверить занятость заданной области
    def empty(self, start_r: int, start_c: int, end_r: int, end_c: int) -> bool:
        # проверяем end_r - start_r + 1 строк
        for i in range(start_r, end_r + 1):
            # проверяем end_c - start_c + 1 столбцов
            for j in range(start_c, end_c + 1):
                if self.brd[i][j] == 1:
                    return False
        return True

    # Попытка расставить корабли
    # 0 = успешно, -1 = не успешно
    def attempt_place_ships(self) -> int:
        ship_count = 0
        for ship_size in range(1, self.ship_types + 1):
            for ship in range(self.ship_types + 1 - ship_size):
                x = self.place_ship(ship_size, choice(['H', 'V']), ship_count)
                if x == -1:
                    self.brd = [[0] * self.all_size for _ in range(self.all_size)]
                    self.ships = []
                    self.ships_map = {}
                    return -1
                ship_count += 1
        return 0

    # Расставить корабли
    # 0 = успешно, -1 = не удалось за attempts попыток
    def place_ships(self, attempts: int) -> int:
        attempt = 0
        while attempt <= attempts:
            if self.attempt_place_ships() == 0:
                return 0
            attempt += 1
            # print(f'Attempt #{attempt}: Can not place {ship + 1}th ship with size {ship_size}')
        return -1

    # Корабли расставляем в полной таблице.
    # Каждый корабль идет вместе с окружающими его пустыми ячейками
    # length = длина корабля
    # direction = направление ('H' - горизонт, 'V' - вертик)
    # num = индекс корабля в списке кораблей
    # Возвращает 0 в случае успешной попытки размещения и
    # -1 в случае неуспешной попытки разместить корабль
    def place_ship(self, length: int, direction: str, num: int) -> int:
        # По умолчанию считаем направление горизонтальным
        # Задаём нижнюю и правую границы области таблицы
        brd_row_bound, brd_col_bound = self.all_size - 3, self.all_size - length - 2
        # Задаем границы макета корабля
        ship_row_bound, ship_col_bound = 3, length + 2
        if direction == 'V':
            brd_row_bound, brd_col_bound = brd_col_bound, brd_row_bound
            ship_row_bound, ship_col_bound = ship_col_bound, ship_row_bound
        # Выбираем из таблицы свободные области под макет корабля
        # В массив areas пишем индекс левой верхней ячейки найденной области
        areas = []
        for brd_rn in range(brd_row_bound + 1):
            for brd_cn in range(brd_col_bound + 1):
                # исследуем область с левой верхней ячейкой (brd_rn, brd_cn)
                if self.empty(brd_rn, brd_cn, brd_rn + ship_row_bound - 1, brd_cn + ship_col_bound - 1):
                    areas.append((brd_rn, brd_cn))
        # проверяем возможность размещения
        if len(areas) == 0:
            return -1
        # Случайно выбираем область размещения
        x, y = choice(areas)
        # добавляем новый корабль в список кораблей
        new_ship = Ship(length, direction, x + 1, y + 1)
        self.ships.append(new_ship)
        # Обновляем информацию на доске
        u, v = x + ship_row_bound - 1, y + ship_col_bound - 1
        for i in range(x, u + 1):
            if i == 0 or i == self.brd_size + 1:
                continue
            for j in range(y, v + 1):
                if j == 0 or j == self.brd_size + 1:
                    continue
                if x < i < u and y < j < v:
                    self.brd[i][j] = 1
                else:
                    new_ship.neighbour_cells.append((i, j))

    # Список допустимых соседних клеток
    def get_neighborhoods(self, row: int, col: int) -> [(int, int)]:
        r = []
        for i in range(row - 1, row + 2):
            if i == 0 or i == self.brd_size + 1:
                continue
            for j in range(col - 1, col + 2):
                if j == 0 or j == self.brd_size + 1 or i == j:
                    continue
                r.append((i, j))
        return r

    # Состояние доски:
    # 0 - играем, 1 - конец игры (все корабли подбиты)
    def brd_state(self) -> int:
        for ship in self.ships:
            if ship.get_state() < 2:
                return 0
        return 1

    # Вывод таблицы
    def prn(self):
        for row in self.brd[1:-1]:
            print(' | '.join(map(lambda x: '*' if x > 0 else '.', row[1:-1])))
        print()


class SeaBattle:
    def __init__(self, board_size: int, ship_types: int):
        self.board_size = board_size
        self.ship_types = ship_types
        # Ходы ироков
        self.moves = [[], []]
        # Игровые доски
        self.player_brd = []
        for _ in range(2):
            self.player_brd.append(Board(board_size, ship_types))
        # Текущий игрок
        self.cur_player = 0

    # Ход игрока
    # self.cur_player выдает координаты позиции
    # 0 - переход хода
    # > 0 - попадание, возвращает на 1 увеличенный индекс подбитого корабля
    def move(self, row: int, col: int) -> int:
        if (row, col) in self.moves[self.cur_player]:
            # игрок указал ранее использованную позицию
            # переход хода
            print(f'Player {self.cur_player} input already used position!')
            return 0
        # фиксируем позицию
        self.moves[self.cur_player].append((row, col))
        # Проверяем попадание
        other_player = 1 - self.cur_player
        item = self.player_brd[other_player].brd[row][col]
        if item == 1:
            # ЕСТЬ ПОПАДАНИЕ!
            # Определяем индекс корабля, в который попали
            hit_ship_idx = self.player_brd[other_player].ships_map[(row, col)]
            # Находим корабль, в который попали
            hit_ship = self.player_brd[other_player].ships[hit_ship_idx]
            # Меняем состояние корабля, в который попали
            hit_ship.hit(row, col)
            # Определяем состояние корабля, в который попали
            hit_ship_state = hit_ship.get_state()
            str_state = 'HALF-LIVE' if hit_ship_state < 2 else 'DEAD'
            print(f'Player {self.cur_player} hit the ship; state of the ship is {str_state}')
            return hit_ship_idx + 1
        return 0

    # Простейший вариант выбора позиции - случайно из неоткрытых клеток доски
    def choice_def_pos(self) -> (int, int):
        return choice([(i, j) for i in range(1, xs) for j in range(1, xs) if (i, j) not in self.moves[1]])

    # Выбор позиции, когда есть одно попадание (открыта одна клетка корабля)
    def choice_4_pos(self, ship: Ship, row: int, col: int) -> (int, int):
        nc = []
        # Ищем не открытые соседние клетки
        for cell in self.player_brd[1].get_neighborhoods(row, col):
            if cell in self.moves[1]:
                continue
            nc.append(cell)
        lnc = len(nc)
        if lnc == 0:
            print(f'ERROR! Can not get next position! Player 1 last position: row={row}, col={col}')
            return self.choice_def_pos()
        return choice(nc)

    # Выбор позиции, когда есть более одного попадания
    # (открыты несколько клеток корабля или клетки разных кораблей)
    def choice_2_pos(self, ship: Ship, row: int, col: int) -> (int, int):
        pass

    # Определение координат следующего удара
    # 1. Если нет попадания - случайный выбор из не открытых ячеек
    # 2. Если есть первое попадание и корабль потоплен (т.е. однопалубный) - просто добавляем его соседние клетки
    # в список открытых клеток и делаем случайный выбор позиции из еще не открытых клеток.
    # 3. Если есть первое попадание корабль не потоплен - выбираем позицию случайно из 4 допустимых клеток
    # 4. Если есть очередное попадание и корабль не потоплен - выбираем позицию в направлении корабля в одном из
    # двух допустимых направлений
    # 5. Если есть очередное попадание и корабль потоплен - делаем как в п.2
    def get_next_pos(self, move_cnt: int, hit_ship_idx: int, row: int, col: int) -> (int, int):
        # 1. Если нет попадания - случайный выбор из неоткрытых ячеек
        if move_cnt == 0:
            return self.choice_def_pos()
        ship_idx = hit_ship_idx - 1
        ship = self.player_brd[1].ships[ship_idx]
        # 2. Если есть первое попадание и корабль потоплен (т.е. однопалубный)
        # 5. Если есть очередное попадание и корабль потоплен
        # Просто добавляем его соседние клетки в список открытых клеток и
        # делаем случайный выбор позиции из еще не открытых клеток.
        if ship.get_state() == 2:
            self.moves[1] += ship.neighbour_cells
            return self.choice_def_pos()
        # 3. Если есть первое попадание и корабль не потоплен (не однопалубный) -
        # выбираем позицию случайно из 4 допустимых клеток
        if move_cnt == 1:
            return self.choice_4_pos(ship, row, col)
        # 4. Если есть очередное попадание и корабль не потоплен -
        # выбираем позицию в направлении корабля в одном из 2 допустимых направлений

    # Анализ текущего положения
    # 0 - играем дальше
    # 1 - конец игры, выиграл первый игрок
    # 2 - конец игры, выиграл второй игрок
    def game_state(self) -> int:
        g_state = (self.player_brd[0].brd_state(), self.player_brd[1].brd_state())
        return g_state[0] + (g_state[1] << 1)

    # Вывод текущего представления доски противника
    # с учетом сделанных ходов текущим игроком
    def prn(self):
        for i, r in enumerate(self.player_brd[1 - self.cur_player].brd[1:-1]):
            rr = []
            for j, v in enumerate(r[1:-1]):
                rr.append(v if (i + 1, j + 1) in self.moves[self.cur_player] else -1)
            print(' | '.join(map(lambda x: '*' if x > 0 else '.' if x == 0 else ' ', rr)))
        print()


if __name__ == "__main__":
    xg = SeaBattle(10, 4)
    xs = xg.board_size + 1
    move_counter = 0
    # вывод информации
    print('Your board:')
    xg.player_brd[0].prn()
    print('Opponent board:')
    xg.player_brd[1].prn()
    r, gs = 0, 0
    p_row, p_col = -1, -1
    while gs == 0:
        if xg.cur_player == 0:
            while p_row < 1 or p_row > xg.board_size:
                p_row = int(input('Введите строку: '))
            while p_col < 1 or p_col > xg.board_size:
                p_col = int(input('Введите столбец: '))
        else:
            # pool = [(i, j) for i in range(1, xs) for j in range(1, xs) if (i, j) not in xg.moves[1]]
            # p_row, p_col = choice(pool)
            p_row, p_col = xg.get_next_pos(move_counter, r, p_row, p_col)
            print(f'Player 1 choices position row = {p_row}, col = {p_col}')
        r = xg.move(p_row, p_col)
        # Выводим для текущего игрока текущую доску противнику
        print('--> Current Opponent board:')
        xg.prn()
        if r == 0:
            # переход хода
            xg.cur_player = 1 - xg.cur_player
            r, move_counter = 0, 0
            p_row, p_col = -1, -1
        else:
            move_counter += 1
        gs = xg.game_state()

    if gs == 1:
        print('Congratulations, You win!')
    else:
        print('Oops, Your Opponent win!')
