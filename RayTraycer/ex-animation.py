from tkinter import *
from time import sleep


def close():
    global running
    running = False


root = Tk()
root.protocol('WM_DELETE_WINDOW', close)
running = True


def ball_jamping():
    ww, wh = 300, 200
    c = Canvas(root, width=ww, height=wh, bg='white', highlightthickness=1)
    c.pack()

    ww2, wh2 = ww >> 1, wh >> 1
    rad = 30
    x0, y0, x1, y1 = 1, wh2 - rad, 1 + (rad << 1), wh2 + rad

    ball = c.create_oval(x0, y0, x1, y1, fill='green', outline='red')
    speed_x, speed_y = 2, 0

    while running:
        c.move(ball, speed_x, speed_y)
        crd = c.coords(ball)
        # скорость вдоль Х
        if crd[0] <= 0 or crd[2] >= ww:
            speed_x = -speed_x
            c.itemconfig(ball, fill='green' if speed_x > 0 else 'red',
                         outline='red' if speed_x > 0 else 'green')
        # скорость вдоль Y
        if crd[3] == y1:
            speed_y = 1
        elif crd[3] >= wh:
            speed_y = -speed_y
        else:
            speed_y += 1
        # цикл
        sleep(0.04)
        root.update()


# Вычисление движения по заданным параметрам и текущему положению
# Вход: массив параметров материальных точек:
# 0 - радиус, 1 - масса
# 2 - координата х, 3 - координата y
# 4 - скорость vx, 5 - скорость vy
# Выход: массив скоростей vx, vy
def calc_moving(points: [[float]]) -> [(float, float)]:
    speeds = []
    for i, point in enumerate(points):
        m, x, y, vx, vy = point[1:]
        # ускорение
        ax, ay = 0, 0
        for j, other_point in enumerate(points):
            if i == j:
                continue
            mo, xo, yo, vxo, vyo = other_point[1:]
            # вектор r(i, j)
            r = (xo - x, yo - y)
            rr = r[0] * r[0] + r[1] * r[1]
            rm = rr ** .5
            # Считаем ускорение, создаваемое точкой j
            a = mo / rr
            # Считаем вклад точки j в ускорение точки i
            ax += a * r[0] / rm
            ay += a * r[1] / rm
        speeds.append((vx + ax, vy + ay))
    return speeds


def planets_moving():
    # выбираем холст
    ww, wh = 900, 900
    c = Canvas(root, width=ww, height=wh, bg='black', highlightthickness=1)
    c.pack()

    ww2, wh2 = ww >> 1, wh >> 1
    ww3, wh3 = ww / 3, wh / 3

    # Параметры
    params = [
        [[20, 10000, ww2, wh2, 0, 0], 'yellow', 'light yellow'],
        # [[10, 100, ww3, wh3, 5, -6], 'blue', 'light blue'],
        [[10, 500, 2 * ww3, 2 * wh3, 5, -2], 'purple', 'medium purple']
    ]

    planets = []
    v_vecs = []
    r_vecs = []

    for param in params:
        r, m, x, y, sx, sy = param[0]
        # рисуем точки
        planets.append(c.create_oval(x - r, y - r, x + r, x + r, fill=param[1], outline=param[2]))
        # отмечаем текущее положение
        c.create_oval(x - 1, y - 1, x + 1, y + 1, fill='red')
        # рисуем вектор скорости
        v_vecs.append(c.create_line(x, y, x + 10 * sx, y + 10 * sy, fill='green',
                                    width=2, arrow=LAST, dash=(10, 2), arrowshape=(6, 10, 6)))
        # рисуем вектор из центра в планету
        xc, yc = params[0][0][2], params[0][0][3]
        r_vecs.append(c.create_line(xc, yc, x, y, fill='red', width=2, arrow=LAST, dash=(10, 2),
                                    arrowshape=(6, 10, 6)))
    # дельта
    tau = 0.07

    # Запускаем расчет
    while running:
        # для каждой планеты рисуем текущее положение
        points = []
        for i, planet in enumerate(planets):
            points.append(params[i][0])
            c.move(planet, params[i][0][4], params[i][0][5])
        # вычисляем новые скорости
        speeds = calc_moving(points)
        for i, planet in enumerate(planets):
            sx, sy = speeds[i]
            # сохраняем новые координаты и новые скорости в массиве params
            crd = c.coords(planet)
            params[i][0][2] = (crd[0] + crd[2]) / 2
            params[i][0][3] = (crd[1] + crd[3]) / 2
            params[i][0][4], params[i][0][5] = sx, sy
            # рисуем точку текущего положения
            x, y = params[i][0][2], params[i][0][3]
            c.create_oval(x - 1, y - 1, x + 1, y + 1, fill=params[i][1])
            # рисуем вектор скорости
            c.coords(v_vecs[i], x, y, x + 10 * sx, y + 10 * sy)
            # рисуем радиус-вектор из центра в точку
            xc, yc = params[0][0][2], params[0][0][3]
            c.coords(r_vecs[i], xc, yc, x, y)
        # проворачиваем цикл
        sleep(tau)
        root.update()


# planets_moving()
# ball_jamping()

root.destroy()
