from tkinter import *


class SudokuGrid:
    def __init__(self):
        self.root = Tk()
        self.root.configure(bg='black')
        #self.frame1 = Frame(self.root)
        #self.frame2 = Frame(self.root)
        #self.frame3 = Frame(self.root)
        self.entry = []
        for i in range(9):
            self.entry.append([])
            for j in range(9):
                self.entry[i].append(Entry(bg='white', width=4, justify=CENTER, relief=GROOVE))
                si, sj = str(i), str(j)
                cmd = 'self.entry[' + si + '][' + sj + '].grid(row=' + si + ', column=' + sj
                if i in (2, 5):
                    cmd += ', pady=(0, 2)'
                if j in (2, 5):
                    cmd += ', padx=(0, 2)'
                cmd += ')'
                eval(cmd)
        # Кнопки
        btn_set = Button(text='Reset', width=14, command=self.reset)
        btn_set.grid(row=10, column=0, columnspan=4, sticky='w', pady=(2, 2))
        btn_reset = Button(text='Ok', width=14, command=self.ok)
        btn_reset.grid(row=10, column=5, columnspan=4, sticky='e')
        # Поля для вывода
        self.ent_j = Text(bg='grey', width=15, height=10, relief=GROOVE, font=('Verdana', 8))
        self.ent_j.grid(row=11, column=0, columnspan=4, sticky='w')
        self.ent_p = Text(bg='grey', width=15, height=10, relief=GROOVE, font=('Verdana', 8))
        self.ent_p.grid(row=11, column=5, columnspan=4, sticky='e')
        self.root.mainloop()

    def reset(self):
        for i in range(9):
            for j in range(9):
                self.entry[i][j].delete(0)
                self.ent_j.delete(1.0, END)
                self.ent_p.delete(1.0, END)

    def ok(self):
        sj, sp = [], []
        for i in range(9):
            m = map(lambda j: self.entry[i][j].get() if self.entry[i][j].get() else '0', range(9))
            sj.append('{' + ','.join(m) + '}')
            m = map(lambda j: self.entry[i][j].get() if self.entry[i][j].get() else '0', range(9))
            sp.append(''.join(m))
        tbl_j = ',\n'.join(sj)
        self.ent_j.focus()
        self.ent_j.insert(1.0, tbl_j)
        tbl_p = '\n'.join(sp)
        self.ent_p.focus()
        self.ent_p.insert(1.0, tbl_p)


sg = SudokuGrid()
