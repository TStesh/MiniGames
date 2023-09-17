from params import G_HEIGHT, G_WIDTH, DX, DY
from tkinter import Label, LEFT, BOTTOM, CENTER, GROOVE


class Glass:

    def __init__(self, f_top, f_bot, canvas, start_btn, pause_btn):
        self.c = canvas
        self.score_fld = Label(
            f_top, text='0', width=DX >> 1,
            fg='yellow', bg='green', justify=CENTER, relief=GROOVE,
            bd=3, font=("Comic Sans MS", DX, "bold")
        )
        f_top.pack()
        start_btn.pack(side=LEFT)
        self.score_fld.pack(side=LEFT)
        pause_btn.pack(side=LEFT)
        f_bot.pack()
        self.c.pack(side=BOTTOM)
        self.g_tbl = [[0] * G_WIDTH for _ in range(G_HEIGHT)]
        self.score = 0

    def check_lines(self):
        lines = []
        for i in range(G_HEIGHT):
            is_full_line = True
            for j in range(G_WIDTH):
                if not self.g_tbl[i][j]:
                    is_full_line = False
                    break
            if is_full_line:
                lines.append(i)
        if lines:
            while lines:
                i = lines.pop()
                self.g_tbl.remove(self.g_tbl[i])
                self.g_tbl.append([0] * G_WIDTH)
                self.score += 1
            self.draw()

    def draw(self):
        for i in range(G_HEIGHT):
            for j in range(G_WIDTH):
                x1, y1 = j * DX, (G_HEIGHT - i - 1) * DY
                x2, y2 = x1 + DX, y1 + DY
                if self.g_tbl[i][j]:
                    self.c.create_rectangle(x1, y1, x2, y2, fill='blue', outline='green', width=1)
                else:
                    self.c.create_rectangle(x1, y1, x2, y2, fill='grey', outline='grey')
        self.score_fld['text'] = str(self.score)

    def check_shape(self, action_type, coords):
        if action_type == 'LEFT':
            for cr in coords:
                x, y, *_ = cr
                i, j = int(x) // DX, G_HEIGHT - int(y) // DY
                if j > G_HEIGHT - 1:
                    continue
                if i == 0 or self.g_tbl[j][i - 1]:
                    return False
            return True
        if action_type == 'RIGHT':
            for cr in coords:
                *_, x, y = cr
                i, j = int(x) // DX - 1, G_HEIGHT - int(y) // DY
                if j > G_HEIGHT - 1:
                    continue
                if i == G_WIDTH - 1 or self.g_tbl[j][i + 1]:
                    return False
            return True
        if action_type == 'DOWN':
            for cr in coords:
                *_, x, y = cr
                i, j = int(x) // DX - 1, G_HEIGHT - int(y) // DY
                if j == 0 or self.g_tbl[j - 1][i]:
                    for crd in coords:
                        *_, sx, sy = crd
                        self.g_tbl[G_HEIGHT - int(sy) // DY][int(sx) // DX - 1] = 1
                    self.check_lines()
                    return False
            return True
