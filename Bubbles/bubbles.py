import sys
from os import path
import base64
import pygame
from random import randint

img_dir = path.join(path.dirname(__file__), 'img')

# Глобальные константы
GRID_SIZE = 10
GRID_ALINE = 2
BALL_ALINE = 10
WINDOW_SIZE = 640
BALLS_COUNT = 9
ADD_BALLS = 3
SAME_BALLS = 5
BALL_VALUE = 10
LINE_VALUE = 8
FPS = 30
JUMP = 5
MOVE = 2
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
dir_names = ('L', 'R', 'U', 'D')
res_file = 'bubbles.res'
CELL = WINDOW_SIZE // GRID_SIZE

# Глобальные объекты
color_map = []
balls = []
colors = [0] * BALLS_COUNT
max_score = 0
score = 0


# Объект сетка
class Grid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = t_img
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y


# Объект шарик
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.color = x, y, color
        self.ix, self.iy = x // CELL, y // CELL
        self.jump_speed = JUMP
        self.jumping = False
        self.move_speed = MOVE
        self.moving = False
        self.move_cells = []
        self.image = balls_img[color]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.left = x + BALL_ALINE // 2
        self.rect.top = y + BALL_ALINE // 2

    def update(self):
        global add_ball_count
        if self.jumping:
            self.rect.top -= self.jump_speed
            self.jump_speed -= 1
            if self.jump_speed == -JUMP:
                self.jump_speed = JUMP - 1
        elif self.moving:
            if self.move_speed > 0:
                self.move_speed -= 1
            else:
                self.move_speed = MOVE - 1
                if self.move_cells:
                    self.ix, self.iy = self.move_cells.pop(0)
                    self.x, self.y = self.ix * CELL, self.iy * CELL
                    self.rect.left = self.x + BALL_ALINE // 2
                    self.rect.top = self.y + BALL_ALINE // 2
                else:
                    self.moving = False
                    # проверяем линии
                    if len([x for x in colors if x >= SAME_BALLS]):
                        lines = check_lines()
                        if len(lines) > 0:
                            delete_lines(lines)
                            add_balls(1)
                            if len([x for x in colors if x >= SAME_BALLS]):
                                lines = check_lines()
                                if len(lines) > 0:
                                    delete_lines(lines)
                        else:
                            add_balls()
                    else:
                        add_balls()
        else:
            # для остальных шариков просто нормализуем положение
            self.rect.left = self.x + BALL_ALINE // 2
            self.rect.top = self.y + BALL_ALINE // 2

    def print(self):
        print('Ball parameters:')
        print('Color:', self.color)
        print('Coords:', self.ix, self.iy)


# Функция получения максимального результата
def get_max_score(filename):
    try:
        f = open(filename, 'rb')
        ms = int(base64.b64decode(f.read()).decode('ascii'))
        f.close()
    except IOError:
        ms = 0
    return ms


# Функция определения наличия шарика в заданной позиции
def is_ball(pos):
    return True if color_map[pos[0]][pos[1]] >= 0 else False


# Функция определения наличия свободных ячеек
def is_free_cells():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if color_map[i][j] == -2:
                return True
    return False


# Функция получения списка свободных ячеек
def get_free_cells():
    s = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if color_map[i][j] == -2:
                s.append((i, j))
    return s


# Функция получения кол-ва занятых ячеек
def num_fill_cells():
    s = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if color_map[i][j] != -2:
                s += 1
    return s


# Функция добавления шариков
def add_balls(num_balls=ADD_BALLS):
    s = get_free_cells()
    s_len = len(s)
    m = s_len if s_len < num_balls else num_balls
    for _ in range(m):
        random_pos = randint(0, s_len - 1) if s_len > 1 else 0
        a, b = s[random_pos]
        s.remove(s[random_pos])
        color = randint(0, BALLS_COUNT - 1)
        ball = Ball(CELL * a, CELL * b, color)
        all_sprites.add(ball)
        balls.append(ball)
        color_map[a][b] = color
        colors[color] += 1
        s_len -= 1


# Вспомогательная функция
def find_all_substrings(src_str):
    res = {}
    for c in set(src_str):
        if c == '-':
            continue
        z = [x for x in enumerate(src_str) if x[1] == c]
        s = []
        trigger = True
        for i in range(z[0][0], z[-1][0] + 1):
            if (i, c) in z:
                if trigger:
                    s.append(i)
                    s.append(i)
                    trigger = False
                s.pop()
                s.append(i)
            else:
                trigger = True
        norm_s = []
        for i in range(0, len(s), 2):
            norm_s.append((s[i], s[i + 1]))
        res[c] = norm_s
    return res


def check_vector(vec):
    v = []
    # нормализация
    t = str(vec).replace('-2', '-').replace('[', '').replace(']', '').replace(',', '').replace(' ', '')
    r = find_all_substrings(t)
    for x in r.keys():
        for _ in r[x]:
            ix, iy = _[0], _[1]
            if iy - ix + 1 >= SAME_BALLS:
                for idx in range(ix, iy + 1):
                    v.append(idx)
    return v


def check_lines():
    global score
    found_pos = []
    num_lines = 0
    for i in range(GRID_SIZE):
        # проверяем горизонтали и вертикали
        s = []
        for j in range(GRID_SIZE):
            s.append(color_map[j][i])
        v1, v2 = check_vector(color_map[i]), check_vector(s)
        if len(v1) > 0:
            num_lines += 1
            for _ in v1:
                found_pos.append((i, _))
        if len(v2) > 0:
            num_lines += 1
            for _ in v2:
                found_pos.append((_, i))
    # проверяем диагонали
    for i in range(SAME_BALLS - 1, GRID_SIZE):
        s1, s2 = [], []
        for j in range(i + 1):
            s1.append(color_map[j][GRID_SIZE + j - i - 1])
            s2.append(color_map[i - j][j])
        v1, v2 = check_vector(s1), check_vector(s2)
        if len(v1) > 0:
            num_lines += 1
            for _ in v1:
                found_pos.append((_, GRID_SIZE + _ - i - 1))
        if len(v2) > 0:
            num_lines += 1
            for _ in v2:
                found_pos.append((i - _, _))
    for i in range(GRID_SIZE - 2, SAME_BALLS - 2, -1):
        s1, s2 = [], []
        for j in range(i + 1):
            s1.append(color_map[GRID_SIZE + j - i - 1][j])
            s2.append(color_map[GRID_SIZE - j - 1][GRID_SIZE + j - i - 1])
        v1, v2 = check_vector(s1), check_vector(s2)
        if len(v1) > 0:
            num_lines += 1
            for _ in v1:
                found_pos.append((GRID_SIZE + _ - i - 1, _))
        if len(v2) > 0:
            num_lines += 1
            for _ in v2:
                found_pos.append((GRID_SIZE - _ - 1, GRID_SIZE + _ - i - 1))
    score += num_lines * LINE_VALUE
    return found_pos


def delete_lines(pos_list):
    global score
    score += len(pos_list) * BALL_VALUE
    b_list = []
    for pos in pos_list:
        for _ in range(len(balls)):
            ball = balls[_]
            if ball.ix == pos[0] and ball.iy == pos[1]:
                color_map[pos[0]][pos[1]] = -2
                colors[ball.color] -= 1
                b_list.append(ball)
    for ball in b_list:
        all_sprites.remove(ball)
        balls.remove(ball)


def get_ball(pos) -> Ball:
    for _ in range(len(balls)):
        ball = balls[_]
        if ball.ix == pos[0] and ball.iy == pos[1]:
            return ball


def get_jumping_ball() -> Ball:
    for _ in range(len(balls)):
        ball = balls[_]
        if ball.jumping:
            return ball


def is_moving_ball():
    for _ in range(len(balls)):
        ball = balls[_]
        if ball.moving:
            return True
    return False


def move_one_step(p, dir):
    res_pos = (-1, -1)
    if dir == UP and p[1] > 0 and color_map[p[0]][p[1] - 1] == -2:
        res_pos = (p[0], p[1] - 1)
    elif dir == DOWN and p[1] < GRID_SIZE - 1 and color_map[p[0]][p[1] + 1] == -2:
        res_pos = (p[0], p[1] + 1)
    elif dir == LEFT and p[0] > 0 and color_map[p[0] - 1][p[1]] == -2:
        res_pos = (p[0] - 1, p[1])
    elif dir == RIGHT and p[0] < GRID_SIZE - 1 and color_map[p[0] + 1][p[1]] == -2:
        res_pos = (p[0] + 1, p[1])
    return res_pos


# Найти путь из from_pos в to_pos
def find_path(from_pos, to_pos):
    DIST_MAX = GRID_SIZE * GRID_SIZE + 1
    counts = [[DIST_MAX] * GRID_SIZE for _ in range(GRID_SIZE)]
    path_from = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    open_list = [from_pos]
    counts[from_pos[0]][from_pos[1]] = 0
    # вычисляем все расстояния от from_pos
    while open_list:
        cur_pos = open_list.pop(0)
        for d in (UP, DOWN, LEFT, RIGHT):
            next_pos = move_one_step(cur_pos, d)
            if next_pos != (-1, -1):
                dist = counts[cur_pos[0]][cur_pos[1]] + 1
                if counts[next_pos[0]][next_pos[1]] > dist:
                    counts[next_pos[0]][next_pos[1]] = dist
                    path_from[next_pos[0]][next_pos[1]] = cur_pos
                    open_list.append(next_pos)
    # Проверяем достижимость
    if counts[to_pos[0]][to_pos[1]] == DIST_MAX:
        return []
    # Формируем обратный путь от to_pos к from_pos
    cell = to_pos
    path = [cell]
    while cell != 0:
        path.append(cell)
        cell = path_from[cell[0]][cell[1]]
    # Возвращаем прямой путь от from_pos к to_pos
    return path[::-1]


def try_move_ball(pos_in, pos_out):
    if pos_in == pos_out or is_ball(pos_out):
        return []
    return find_path(pos_in, pos_out)


def parse_mouse_click(coords):
    # проверяем есть ли у нас перемещение шарика
    # если есть, продолжаем перемещение
    if is_moving_ball():
        return
    # определяем ячейку на которой кликнули мышкой
    new_pos = coords.pos[0] // CELL, coords.pos[1] // CELL
    # находим прыгающий шарик
    mark_ball = get_jumping_ball()
    # в ячейке, на которой кликнули, может быть шарик
    new_ball = get_ball(new_pos)
    if new_ball:
        new_ball.jumping = True
        if mark_ball:
            mark_ball.jumping = False
    else:
        if mark_ball:
            # Проверяем возможность переместить шарик
            path = try_move_ball((mark_ball.ix, mark_ball.iy), new_pos)
            if not path:
                return
            # Возможность есть, запускаем перемещение шарика
            mark_ball.jumping = False
            mark_ball.moving = True
            mark_ball.move_cells = path
            color = color_map[mark_ball.ix][mark_ball.iy]
            color_map[mark_ball.ix][mark_ball.iy] = -2
            color_map[new_pos[0]][new_pos[1]] = color


def get_capture_str(init=False):
    global max_score, score
    x = num_fill_cells()
    y = GRID_SIZE * GRID_SIZE - x
    caption_str = 'BUBBLES      <max score: ' + str(max_score) + ', current score: ' + str(score)
    caption_str += '>       <fill cells: ' + str(x) + ', free cells: ' + str(y) + '>'
    return caption_str


# Определение кнопки
def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 50)
    text_render = font.render(text, True, RED)
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
    return screen.blit(text_render, (x, y))


# Старт игры
def start_game():
    global color_map, balls, colors, score, max_score
    # Инициализируем глобальные переменные
    color_map = []
    balls = []
    colors = [0] * BALLS_COUNT
    max_score = get_max_score(res_file)
    score = 0
    # Инициализируем грид
    for k in range(GRID_SIZE):
        pos_x = k * CELL
        color_map.append([-2] * GRID_SIZE)
        for m in range(GRID_SIZE):
            all_sprites.add(Grid(pos_x, m * CELL))
    # Добавляем шарики
    add_balls()
    # Отображаем на экране
    pygame.display.update()
    # Запускаем основной цикл
    running = True
    while running:
        clock.tick(FPS)
        if not is_free_cells():
            running = False
            continue
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False
                continue
            # проверить клик мышки
            elif event.type == pygame.MOUSEBUTTONDOWN:
                parse_mouse_click(event)
        pygame.display.set_caption(get_capture_str())
        all_sprites.update()
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.update()
    # Сохраняем результат если он лучше максимального
    if score > max_score:
        f = open(res_file, 'wb')
        f.write(base64.b64encode(str(score).encode('ascii')))
        f.close()
    # Запускаем кнопки
    show_buttons()


# Кнопки
def show_buttons():
    BTN_ALLIGN = 100
    BTN_H_START = WINDOW_SIZE // 2
    BTN_W_START = WINDOW_SIZE // 2 - BTN_ALLIGN

    btn_start = button(screen, (BTN_W_START, BTN_H_START), "Start")
    btn_quit = button(screen, (BTN_W_START + 2 * BTN_ALLIGN, BTN_H_START), "Quit")

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                key_to_start = event.key == pygame.K_s or event.key == pygame.K_RIGHT or event.key == pygame.K_UP
                if key_to_start:
                    start_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_start.collidepoint(pygame.mouse.get_pos()):
                    start_game()
                elif btn_quit.collidepoint(pygame.mouse.get_pos()):
                    running = False
        pygame.display.update()
    sys.exit()


# ========================================================================================================
# ЗАПУСК ИГРЫ
# Инициализируем графику
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()

# Создаем группу спрайтов игры
all_sprites = pygame.sprite.Group()

# Загружаем картинку плитки грида
t_img = pygame.image.load(path.join(img_dir, 'tail2.jpg')).convert()
t_img = pygame.transform.scale(t_img, (CELL - GRID_ALINE, CELL - GRID_ALINE))

# Загружаем картинки шариков
balls_img = []
for k in range(BALLS_COUNT):
    b_img = pygame.image.load(path.join(img_dir, 'sphere' + str(k + 1) + '.png')).convert()
    b_img = pygame.transform.scale(b_img, (CELL - BALL_ALINE, CELL - BALL_ALINE))
    balls_img.append(b_img)

# Запускаем игру
start_game()
