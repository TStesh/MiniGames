from random import choice

heights = [9, 16, 16]
widths = [9, 16, 30]
bombs_count = [10, 40, 90]

MINE = -1
EMPTY = 0

Cell = (int, int)


class Board:

    def __init__(self, skill: int):
        self.hc = heights[skill]
        self.wc = widths[skill]
        self.mc = bombs_count[skill]
        self.mines = self.gen_mines_places()
        self.brd = [[0] * self.wc for _ in range(self.hc)]
        for r in range(self.hc):
            for c in range(self.wc):
                if self.brd[r][c] in self.mines:
                    self.brd[r][c] = MINE
                for x in [_ for _ in self.get_neighbor8_cells((r, c)) if _ in self.mines]:
                    self.brd[x[0]][x[1]] = MINE
                    self.brd[r][c] += 1

    # Сгенерировать расположение мин
    def gen_mines_places(self) -> [Cell]:
        mp = []
        pool = [(i, j) for i in range(self.hc) for j in range(self.wc)]
        for _ in range(self.mc):
            x = choice(pool)
            mp.append(x)
            pool.remove(x)
        return mp

    # Значение в клетке
    def val(self, cell: Cell) -> int:
        return self.brd[cell[0]][cell[1]]

    # Мина?
    def is_mine(self, cell: Cell) -> bool:
        return self.brd[cell[0]][cell[1]] == MINE

    # Пустая?
    def is_free(self, cell: Cell) -> bool:
        return self.brd[cell[0]][cell[1]] == EMPTY

    # Cоседние клетки по всем направлениям:
    def get_neighbor8_cells(self, cell: Cell):
        n_cells = []
        for i in range(cell[0] - 1, cell[0] + 2):
            if i < 0 or i >= self.hc:
                continue
            for j in range(cell[1] - 1, cell[1] + 2):
                if j < 0 or j >= self.wc or (i == cell[0] and j == cell[1]):
                    continue
                n_cells.append((i, j))
        return n_cells

    # Соседние клетки по 4 стандартным направлениям:
    def get_neighbor4_cells(self, cell: Cell):
        cells = [(cell[0] - 1, cell[1]), (cell[0] + 1, cell[1]),
                 (cell[0], cell[1] - 1), (cell[0], cell[1] + 1)]
        n_cells = []
        for x, y in cells:
            if x < 0 or x >= self.hc or y < 0 or y >= self.wc:
                continue
            n_cells.append((x, y))
        return n_cells

    # Список пустых клеток
    def get_free_cells(self, cells: [Cell], free_cells: [Cell]) -> [Cell]:
        if len(cells) == 0:
            return free_cells
        new_cells = []
        for cell in cells:
            if cell in free_cells or not self.is_free(cell):
                continue
            free_cells.append(cell)
            for y in self.get_neighbor4_cells(cell):
                if y in free_cells or y in cells:
                    continue
                if self.is_free(y):
                    new_cells.append(y)
        return self.get_free_cells(new_cells, free_cells)

    # Печать доски
    def brd_prn(self):
        t0 = len(str(self.hc))
        for k, row in enumerate(self.brd):
            s = ' | '.join(map(lambda x: str(x) if x > 0 else '.' if x == 0 else '*', row))
            ks = str(k)
            t = ' ' * (t0 - len(ks)) + ks
            print(f'{t}: {s}')
