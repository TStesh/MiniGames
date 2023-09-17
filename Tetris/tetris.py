from tkinter import Tk, Frame, Canvas, Button
from params import cur_tick, DX, DY, G_WIDTH, G_HEIGHT
from shape import Shape
from glass import Glass

is_pause = False
is_start = False
is_fast = False

def start():
    global is_start
    is_start = True
    motion_down(1, cur_tick)

def pause():
    global is_pause
    is_pause = not is_pause

def set_is_fast():
    global is_fast
    is_fast = True


root = Tk()
root.title('TETRIS')

f_top, f_bot = Frame(), Frame()
c = Canvas(f_bot, width=G_WIDTH * DX, height=G_HEIGHT * DY, bg='grey')
start_btn = Button(f_top, text='Start', width=DX >> 1, font=("Comic Sans MS", DX, "bold"), command=start)
pause_btn = Button(f_top, text='Pause', width=DX >> 1, font=("Comic Sans MS", DX, "bold"), command=pause)

g = Glass(f_top, f_bot, c, start_btn, pause_btn)

c.focus_set()

s = Shape(c)

def motion_left():
    if is_start and not is_pause and g.check_shape('LEFT', s.get_coords()):
        s.move_left()

def motion_right():
    if is_start and not is_pause and g.check_shape('RIGHT', s.get_coords()):
        s.move_right()

def motion_down(trigger, delay):
    global s, is_fast
    if trigger:
        s.draw()
    if is_fast:
        delay = 1
    if not is_pause:
        if g.check_shape('DOWN', s.get_coords()):
            s.move_down()
        else:
            s = Shape(c)
            s.draw()
            delay = cur_tick
            is_fast = False
    root.after(delay, lambda: motion_down(0, delay))

c.bind('<Right>', lambda event: motion_right())
c.bind('<Left>', lambda event: motion_left())
c.bind('<space>', lambda event: set_is_fast())
c.bind('<z>', lambda event: s.clock_rotate(1))
c.bind('<x>', lambda event: s.clock_rotate(-1))

root.mainloop()
