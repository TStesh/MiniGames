from random import randint
from Games.Tetris import colors
from params import G_WIDTH, DX, DY

shp = [
    # Straight
    [(-1, 0), (0, 0), (1, 0), (2, 0)],
    # Square
    [(0, 0), (0, 1), (-1, 0), (-1, 1)],
    # T
    [(-1, 0), (0, 0), (1, 0), (0, -1)],
    # L
    [(-1, 0), (0, 0), (1, 0), (1, -1)],
    # Reflect L
    [(-1, 0), (0, 0), (1, 0), (-1, -1)],
    # Skew
    [(-1, 0), (0, 0), (0, -1), (1, -1)],
    # Reflect Skew
    [(-1, -1), (0, -1), (0, 0), (1, 0)]
]

class Shape:

    def __init__(self, canvas):
        self.shape_canvas = canvas
        self.shape_type = shp[randint(0, len(shp) - 1)]
        self.fill_clr = colors.COLORS[randint(0, len(colors.COLORS) - 1)]
        self.out_clr = colors.COLORS[randint(0, len(colors.COLORS) - 1)]
        self.cur_x, self.cur_y = G_WIDTH >> 1, 0
        self.shape = []

    def draw(self):
        for dx, dy in self.shape_type:
            x, y = (self.cur_x + dx) * DX, (self.cur_y + dy) * DY
            sb = self.shape_canvas.create_rectangle(
                x, y, x + DX, y + DY,
                fill=self.fill_clr,
                outline=self.out_clr,
                width=1
            )
            self.shape.append(sb)

    def erase(self):
        for sb in self.shape:
            self.shape_canvas.delete(sb)
        self.shape = []

    def move_down(self):
        for shape_elem in self.shape:
            self.shape_canvas.move(shape_elem, 0, DY)
        self.cur_y += 1

    def move_left(self):
        for shape_elem in self.shape:
            self.shape_canvas.move(shape_elem, -DX, 0)
        self.cur_x -= 1

    def move_right(self):
        for shape_elem in self.shape:
            self.shape_canvas.move(shape_elem, DX, 0)
        self.cur_x += 1

    def get_coords(self):
        crds = []
        for sb in self.shape:
            crds.append(self.shape_canvas.coords(sb))
        return crds

    def clock_rotate(self, spin: int):
        new_shape_type = []
        for dx, dy in self.shape_type:
            new_shape_type.append((dy * spin, -dx * spin))
        self.shape_type = new_shape_type
        self.erase()
        self.draw()
