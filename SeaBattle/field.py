from tkinter import *
from time import sleep


class App(Tk):
    w, h = 1000, 600

    def __init__(self, size: int):
        Tk.__init__(self)
        self.title('See Battle')
        self.geometry(str(self.w) + 'x' + str(self.h) + '+100+100')
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.size = size
        self.running = True

        self.img_cell = PhotoImage(file='cell.png')

        self.left_frame = LabelFrame(self, relief='ridge', padx=5, pady=5, text='Opponent Board', font=('Calibri', 14))

        for i in range(size):
            for j in range(size):
                l = Label(self.left_frame, fg='black', borderwidth=0, image=self.img_cell)
                l.grid(row=i, column=j, sticky='nsew')

        # l = Label(fg='black', borderwidth=3)
        # l.grid(row=0, rowspan=size, column=size, sticky='nsew')

        self.right_frame = LabelFrame(self, relief='ridge', padx=5, pady=5, text='Your Board', font=('Calibri', 14))

        for i in range(size):
            for j in range(size):
                l = Label(self.right_frame, fg='black', borderwidth=0, image=self.img_cell)
                l.grid(row=i, column=j, sticky='nsew')

        self.left_frame.place(x=50, y=50)
        self.right_frame.place(x=550, y=50)

    def close(self):
        self.running = False
        self.destroy()


if __name__ == '__main__':
    my_app = App(10)
    my_app.mainloop()
