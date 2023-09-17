from tkinter import *
from tkinter import ttk

from Games.Minesweeper.board import Board, Cell
from Games.Minesweeper.results import Results


class Minesweeper(Tk):
    __MAX_TIME__ = 3598
    __geometry__ = "200x30"
    __offset__ = "+600+300"
    __skill_name__ = ('Новичок', 'Опытный', 'Эксперт')

    def __init__(self, skill: int, db: Results):

        Tk.__init__(self)

        # Загружаем иконки
        self.img_cell = PhotoImage(file='img\\cell.png')
        self.img_flag = PhotoImage(file='img\\flag.png')
        self.img_bad_flag = PhotoImage(file='img\\bad_flag.png')
        self.img_bomb = PhotoImage(file='img\\bomb.png')
        self.img_dot = PhotoImage(file='img\\timer-dot.png')
        self.img_smile_norm = PhotoImage(file='img\\smile-norm.png')
        self.img_smile_sad = PhotoImage(file='img\\smile-sad.png')
        self.img_smile_happy = PhotoImage(file='img\\smile-happy.png')
        self.img_cell_first = PhotoImage(file='img\\cell-first.png')
        self.img_cell_w = PhotoImage(file='img\\cell-w.png')
        self.img_cell_last = PhotoImage(file='img\\cell-last.png')
        self.img_cell_top = PhotoImage(file='img\\cell-top.png')
        self.img_cell_h = PhotoImage(file='img\\cell-h.png')
        self.img_cell_h1 = PhotoImage(file='img\\cell-h1.png')
        self.img_cell_h2 = PhotoImage(file='img\\cell-h2.png')
        self.img_cell_bottom = PhotoImage(file='img\\cell-bottom.png')
        self.img_dig = [PhotoImage(file='img\\digit-' + str(_) + '.png') for _ in range(9)]
        self.img_bdig = [PhotoImage(file='img\\timer-' + str(_) + '.png') for _ in range(10)]

        # Задаем шрифты
        self.font_norm = ('Arial', 12)
        self.font_bold = ('Arial', 12, 'bold')

        # объявляем переменные
        self.skill = skill
        self.db = db
        self.b = None
        self.flags = None
        self.all_cells_amount = None
        self.bomb_amount = None
        self.open_cells = None
        self.labels = None
        self.timer = None
        self.btn = None
        self.game_end = None
        self.counter = None
        self.is_first_click = None
        self.rwm = None
        self.tbl = None
        self.user_name = None
        self.user_name_window = None

        # отображаем меню выбора уровня
        self.geometry(self.__geometry__ + self.__offset__)
        self.title("Главное окно")
        m = Menu(self)
        self.config(menu=m)
        skill_menu = Menu(m, tearoff=0)
        for i in range(3):
            skill_menu.add_command(label=self.__skill_name__[i], command=lambda f=i: self.start_game(f))
        m.add_cascade(label='Уровень', menu=skill_menu)
        m.add_command(label='Рекорды', command=self.show_rec_table)

    # Показать таблицу рекордов
    def show_rec_table(self):
        if self.tbl is not None:
            self.tbl.destroy()
            self.tbl = None
        self.tbl = Toplevel(self, background='#47ffff', padx=5, pady=5)
        self.tbl.geometry(self.__offset__)
        self.tbl.title('Таблица рекордов')
        # получить записи
        recs = self.db.get_records()
        # вывод меню
        mm = Menu(self.tbl)
        self.tbl.config(menu=mm)
        if recs:
            mm.add_command(label='Очистить таблицу', state='normal', command=self.clear_rec_table)
        else:
            mm.add_command(label='Очистить таблицу', state='disabled', command=self.clear_rec_table)
        # вывод заголовка
        hdr = ('Имя', 'Уровень', 'Длительность', 'Дата и время')
        t = ttk.Treeview(self.tbl, columns=hdr, show='headings')
        for h in hdr:
            t.column(h, anchor=CENTER)
            t.heading(h, text=h)
        t.pack()
        # Вывод записей
        for i, rec in enumerate(recs):
            t.insert(values=(rec[0], self.__skill_name__[rec[1]], str(rec[2]), rec[3]), index='end', parent='')

    # Очистить таблицу рекордов
    def clear_rec_table(self):
        db.clear_records()
        self.show_rec_table()

    # Запуск игры
    def start_game(self, skill: int):
        if self.rwm is None:
            # Гасим основное окно
            self.wm_withdraw()
            # Создаем окно для игры
            self.rwm = Toplevel(self)
            self.rwm.geometry(self.__offset__)
            # Выводим заголовок
            self.rwm.title('Сапер (' + self.__skill_name__[skill] + ')')
            # Создаем обработчик события закрытия окна
            self.rwm.protocol('WM_DELETE_WINDOW', self.on_closing)

        # Загружаем доску
        self.b = Board(skill)

        # Инициализируем переменные
        self.skill = skill
        self.flags = []
        self.open_cells = []
        self.labels = []
        self.timer = []
        self.bomb_amount = []
        self.all_cells_amount = self.b.hc * self.b.wc
        self.game_end = False
        self.is_first_click = False
        self.counter = 0

        # рисуем границы
        self.show_w_border(0)
        self.show_h_border(0)
        self.show_h_border(self.b.wc + 1)

        # рисуем таймер
        l_dot = Label(self.rwm, image=self.img_dot, borderwidth=0)
        l_dot.grid(row=1, column=3, sticky=N + S + W + E)

        for i in range(5):
            if i != 2:
                l = Label(self.rwm, image=self.img_bdig[0], borderwidth=0)
                l.grid(row=1, column=i + 1, sticky=N + S + W + E)
                self.timer.append(l)

        # рисуем псевдокнопку рестарта игры
        self.btn = Label(self.rwm, image=self.img_smile_norm, borderwidth=0)
        self.btn.grid(row=1, column=2 + (self.b.wc >> 1), sticky=N + S + W + E)
        self.btn.bind('<Button-1>', lambda e, f=skill: self.start_game(f))

        # рисуем счетчик мин
        x = divmod(self.b.mc, 10)
        for i in range(2):
            l = Label(self.rwm, image=self.img_bdig[x[i]], borderwidth=0)
            l.grid(row=1, column=self.b.wc - 1 + i, sticky=N + S + W + E)
            self.bomb_amount.append(l)

        # рисуем границу
        self.show_w_border(2)

        # Рисуем клетки
        for i in range(self.b.hc):
            l_row = []
            for j in range(self.b.wc):
                l = Label(self.rwm, image=self.img_cell, borderwidth=0)
                l.grid(row=i + 3, column=j + 1, sticky=N + S + W + E)
                l.bind('<Button-1>', lambda e, f=(i, j): self.show_cell(f))
                l.bind('<Button-3>', lambda e, f=(i, j): self.set_flag(f))
                l_row.append(l)
            self.labels.append(l_row)

        # рисуем границу
        self.show_w_border(self.b.hc + 3)

    # Событие закрытия игрового окна
    def on_closing(self):
        if self.rwm is not None:
            self.rwm.destroy()
            self.wm_deiconify()
            self.rwm = None
        else:
            self.destroy()

    # Завершить игру
    # state = True - success
    # state = False - failure
    def end_game(self, state: bool):
        self.game_end = True
        self.btn['image'] = self.img_smile_happy if state else self.img_smile_sad
        # Получить имя и сохранить результат
        if state:
            if self.user_name is None:
                self.user_name_window = Toplevel(self, padx=5, pady=5)
                self.user_name_window.geometry(self.__offset__)
                l = Label(self.user_name_window, text='Имя:', font=self.font_norm)
                l.grid(row=0, column=0, padx=3, pady=10, sticky=W)
                e = Entry(self.user_name_window, width=20, font=self.font_norm)
                e.grid(row=0, column=1, padx=3, pady=10, sticky=W)
                e.bind('<Return>', lambda f: self.save_result(f))
            else:
                self.save_result(None)

    # Сохранить результат
    def save_result(self, f):
        if self.user_name is None:
            self.user_name = f.widget.get().strip()
            if len(self.user_name) > 20:
                self.user_name = self.user_name[:20]
            self.user_name_window.destroy()
            self.user_name_window = None
        db.save_rec(self.user_name, self.skill, self.counter)

    # нарисовать w-границу
    def show_w_border(self, r: int):
        l = Label(self.rwm, image=self.img_cell_first, borderwidth=0)
        l.grid(row=r, column=1, sticky=N + S + W + E)
        for i in range(self.b.wc - 1):
            l = Label(self.rwm, image=self.img_cell_w, borderwidth=0)
            l.grid(row=r, column=i + 1, sticky=N + S + W + E)
        l = Label(self.rwm, image=self.img_cell_last, borderwidth=0)
        l.grid(row=r, column=self.b.wc, sticky=N + S + W + E)

    # нарисовать h-границу
    def show_h_border(self, c: int):
        l = Label(self.rwm, image=self.img_cell_top, borderwidth=0)
        l.grid(row=0, column=c, sticky=N + S + W + E)
        l = Label(self.rwm, image=self.img_cell_h1, borderwidth=0)
        l.grid(row=1, column=c, sticky=N + S + W + E)
        l = Label(self.rwm, image=self.img_cell_h2, borderwidth=0)
        l.grid(row=2, column=c, sticky=N + S + W + E)
        for i in range(self.b.hc):
            l = Label(self.rwm, image=self.img_cell_h, borderwidth=0)
            l.grid(row=i + 3, column=c, sticky=N + S + W + E)
        l = Label(self.rwm, image=self.img_cell_bottom, borderwidth=0)
        l.grid(row=self.b.hc + 3, column=c, sticky=N + S + W + E)

    # Таймер
    def timer(self):
        if self.counter <= self.__MAX_TIME__:
            if self.is_first_click and not self.game_end:
                self.counter += 1
                mm, ss = divmod(self.counter, 60)
                m1, m2 = divmod(mm, 10)
                s1, s2 = divmod(ss, 10)
                for k, x in enumerate([m1, m2, s1, s2]):
                    self.timer[k]['image'] = self.img_bdig[x]
        else:
            self.end_game(False)
        self.rwm.after(1000, self.timer)

    # открыть клетку
    def open_cell(self, cell: Cell):
        if cell in self.open_cells:
            return
        self.labels[cell[0]][cell[1]]['image'] = self.img_dig[self.b.val(cell)]
        self.open_cells.append(cell)
        # проверяем на конец игры
        # если число открытых + число флажков = полному кол-ву клеток
        # и число флажков = равно числу мин, то это победа
        lf = len(self.flags)
        lo = len(self.open_cells)
        if lo + lf == self.all_cells_amount and lf == self.b.mc:
            self.end_game(True)

    # Поставить флажок
    def set_flag(self, cell: Cell):
        if self.game_end:
            return
        if cell in self.open_cells:
            return
        if cell in self.flags:
            self.labels[cell[0]][cell[1]]['image'] = self.img_cell
            self.flags.pop(self.flags.index(cell))
        else:
            self.labels[cell[0]][cell[1]]['image'] = self.img_flag
            self.flags.append(cell)
        # активировать таймер
        if not self.is_first_click:
            self.is_first_click = True
        # отобразить текущее значение счетчика мин
        x = divmod(self.b.mc - len(self.flags), 10)
        for i in range(2):
            self.bomb_amount[i]['image'] = self.img_bdig[x[i]]

    # Показать клетку(и)
    def show_cell(self, cell: Cell):
        if self.game_end:
            return
        # активировать таймер
        if not self.is_first_click:
            self.is_first_click = True
        # если на клетке флажок - ничего не делаем
        if cell in self.flags:
            return
        # если клетка открыта, то открываем соседние клетки
        if cell in self.open_cells:
            self.open_neighbor_cells(cell)
            return
        # клетка закрыта и не под флажком -> открываем ее
        # (*) если там мина, то б-а-а-а-м!
        if self.b.is_mine(cell):
            # открыть все клетки без признака флага
            self.open_all_cells()
            return
        # если клетка пустая, то рисуем пустые клетки
        if self.b.is_free(cell):
            self.open_empty_cells(cell)
            return
        self.open_cell(cell)

    # открыть пустые клетки
    def open_empty_cells(self, cell: Cell):
        xs = self.b.get_free_cells([cell], [])
        for x in [_ for _ in xs if _ not in self.flags]:
            self.open_cell(x)
            # еще нужно открыть неоткрытые клетки, пограничные к пустым
            ys = self.b.get_neighbor8_cells(x)
            for y in [_ for _ in ys if _ not in self.open_cells and self.b.val(_) > 0]:
                self.open_cell(y)

    # Открыть соседние клетки
    def open_neighbor_cells(self, cell: Cell):
        # клетка пустая?
        if self.b.is_free(cell):
            return
        # сколько клеток открыто вокруг?
        ys = self.b.get_neighbor8_cells(cell)
        ys_opens = [_ for _ in ys if _ in self.open_cells]
        # открыты все?
        if len(ys_opens) == 8:
            return
        ys_not_opens = [_ for _ in ys if ys not in ys_opens]
        # сколько прикрыто флажками?
        ys_flags = [_ for _ in ys_not_opens if _ in self.flags]
        if len(ys_flags) != self.b.val(cell):
            return
        # можно открыть не открытые не прикрытые флажками
        ys_not_flags = [_ for _ in ys_not_opens if _ not in ys_flags]
        for x in ys_not_flags:
            if self.b.is_mine(x):
                self.open_all_cells()
            elif self.b.is_free(x):
                self.open_empty_cells(x)
            else:
                self.open_cell(x)

    # Открыть все клетки
    def open_all_cells(self):
        for r in range(self.b.hc):
            for c in range(self.b.wc):
                cell = (r, c)
                if cell in self.open_cells:
                    continue
                if cell in self.flags:
                    if not self.b.is_mine(cell):
                        self.labels[r][c]['image'] = self.img_bad_flag
                else:
                    if self.b.is_mine(cell):
                        self.labels[r][c]['image'] = self.img_bomb
                    else:
                        self.open_cell(cell)
        self.end_game(False)


# Timer
def timer():
    if app.rwm is not None:
        if app.counter <= app.__MAX_TIME__:
            if app.is_first_click and not app.game_end:
                app.counter += 1
                mm, ss = divmod(app.counter, 60)
                m1, m2 = divmod(mm, 10)
                s1, s2 = divmod(ss, 10)
                for k, x in enumerate([m1, m2, s1, s2]):
                    app.timer[k]['image'] = app.img_bdig[x]
        else:
            app.end_game(False)
    app.after(1000, timer)


if __name__ == "__main__":
    db = Results()
    app = Minesweeper(1, db)
    app.after(1000, timer)
    app.mainloop()
