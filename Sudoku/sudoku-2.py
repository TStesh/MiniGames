# Классический судоку
from copy import deepcopy

all_boards = []


def get_suit_digits(arr: [int]) -> {int}:
    return set(range(10)).difference(set(arr))


class Board:
    def __init__(self, board: [[int]]):
        self.board = board

    def print_board(self) -> None:
        for row in self.board:
            print(row)
        print()

    def row(self, i) -> [int]:
        return self.board[i]

    def col(self, i) -> [int]:
        return [self.board[_][i] for _ in range(9)]

    def sub_box(self, row: int, col: int) -> [int]:
        r = []
        a, b = row - row % 3, col - col % 3
        for i in range(a, a + 3):
            for j in range(b, b + 3):
                r.append(self.board[i][j])
        return r

    def get_null_cells(self) -> [(int, int)]:
        r = []
        for i, row in enumerate(self.board):
            for j, digit in enumerate(row):
                if digit == 0:
                    r.append((i, j))
        return r

    def get_suit_digits_set(self, i, j) -> {int}:
        a = get_suit_digits(self.row(i))
        b = get_suit_digits(self.col(j))
        c = get_suit_digits(self.sub_box(i, j))
        return a.intersection(b).intersection(c)

    def process_board(self) -> (int, int):
        while 1:
            m, u, v = 10, -1, -1
            ns = self.get_null_cells()
            if len(ns) == 0:
                return 10, 10
            for i, j in ns:
                sx = self.get_suit_digits_set(i, j)
                x = len(sx)
                if x == 0:
                    return -1, -1
                if x == 1:
                    self.board[i][j] = sx.pop()
                if x < m:
                    m, u, v = x, i, j
            if m > 1:
                break
        return u, v


def solve_sudoku(board: [[int]]) -> [[int]]:
    global all_boards

    all_boards = [Board(board)]

    while 1:
        new_all_boards = []
        for b in all_boards:
            u, v = b.process_board()
            if (u, v) == (10, 10):
                return b
            if (u, v) == (-1, -1):
                continue
            for d in b.get_suit_digits_set(u, v):
                new_board = deepcopy(b.board)
                new_board[u][v] = d
                new_all_boards.append(Board(new_board))
        all_boards = new_all_boards


res_brd = solve_sudoku(
    [[0, 0, 9, 7, 4, 8, 0, 0, 0],
     [7, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 2, 0, 1, 0, 9, 0, 0, 0],
     [0, 0, 7, 0, 0, 0, 2, 4, 0],
     [0, 6, 4, 0, 1, 0, 5, 9, 0],
     [0, 9, 8, 0, 0, 0, 3, 0, 0],
     [0, 0, 0, 8, 0, 3, 0, 2, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 6],
     [0, 0, 0, 2, 7, 5, 9, 0, 0]]
)

res_brd.print_board()
