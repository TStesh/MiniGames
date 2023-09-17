from tkinter import *

path = 'C:\\Users\\alexa\\Documents\\icons\\timer-'

start = False

root = Tk()

img_dot = PhotoImage(file=path + 'dot.png')
img_no_dot = PhotoImage(file=path + 'no-dot.png')

img_dig = []
for _ in range(10):
    img_dig.append(PhotoImage(file=path + str(_) + '.png'))

labels = []

l_dot = Label(root, image=img_dot, borderwidth=0)
l_dot.grid(row=0, column=2, sticky=N + S + W + E)

for i in range(5):
    if i != 2:
        l = Label(root, image=img_dig[0], borderwidth=0)
        l.grid(row=0, column=i, sticky=N + S + W + E)
        labels.append(l)


def show_time(n: int) -> None:
    m, s = divmod(n, 60)
    m1, m2 = divmod(m, 10)
    s1, s2 = divmod(s, 10)
    for k, x in enumerate([m1, m2, s1, s2]):
        labels[k]['image'] = img_dig[x]
    return None


def start_timer():
    global start, root
    start = not start
    counter = 0
    while start and counter <= 5959:
        counter += 1
        root.after(1000, show_time(counter))
        root.update()
    return None


b = Button(root, text='Start', command=start_timer)
b.grid(row=1, column=0, columnspan=3)

root.mainloop()
