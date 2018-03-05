from tkinter import Tk, Canvas, mainloop, NW
from PIL import Image, ImageTk

#размер карты в пикселях
window_width = 600
window_height = 600

bullets = []

#карта
game_map = [ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
             [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
             [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ]

#размеры блока
block_width = window_width // 12
block_height = window_height // 12

#создаем холст
tk = Tk()
c = Canvas(tk, width=window_width, height=window_height, bg='white')
c.pack()

#картинки со стеной и травой
brick = ImageTk.PhotoImage((Image.open("brick.gif").resize((block_width, block_height))))
grass = ImageTk.PhotoImage((Image.open("grass.gif").resize((block_width, block_height))))

#рисуем карту
for i in range(12):
    for j in range(12):
        if game_map[i][j] == 0:
            c.create_image(i * block_width, j * block_height, image=grass, anchor=NW)
        if game_map[i][j] == 1:
            c.create_image(i * block_width, j * block_height, image=brick, anchor=NW)

#картинка с игроком
player_image_up = ImageTk.PhotoImage((Image.open("tank.gif").convert('RGBA').resize((block_width, block_height))))
player_image_down = ImageTk.PhotoImage((Image.open("tank.gif").convert('RGBA').resize((block_width, block_height)).rotate(180)))
player_image_right = ImageTk.PhotoImage((Image.open("tank.gif").convert('RGBA').resize((block_width, block_height)).rotate(270)))
player_image_left = ImageTk.PhotoImage((Image.open("tank.gif").convert('RGBA').resize((block_width, block_height)).rotate(90)))
mine_image_right = ImageTk.PhotoImage((Image.open("mine.gif").convert('RGBA').resize((block_width, block_height))))
mine_image_up = ImageTk.PhotoImage((Image.open("mine.gif").convert('RGBA').resize((block_width, block_height)).rotate(90)))
mine_image_left = ImageTk.PhotoImage((Image.open("mine.gif").convert('RGBA').resize((block_width, block_height)).rotate(180)))
mine_image_down = ImageTk.PhotoImage((Image.open("mine.gif").convert('RGBA').resize((block_width, block_height)).rotate(270)))


def rotate(object, direction):
    # реализуйте функцию поворота танка/пули
    c.itemconfig(object['left'], state='hidden')
    c.itemconfig(object['right'], state='hidden')
    c.itemconfig(object['down'], state='hidden')
    c.itemconfig(object['up'], state='hidden')
    c.itemconfig(object[direction], state='normal')
    
    object['direction'] = direction


def move(object, dx, dy):
    # реализуйте функцию передвижения танка/пули на заданное число пикселей
    c.move(object['left'], dx, dy)
    c.move(object['right'], dx, dy)
    c.move(object['up'], dx, dy)
    c.move(object['down'], dx, dy)


def delete(object):
    c.delete(object['left'])
    c.delete(object['right'])
    c.delete(object['up'])
    c.delete(object['down'])

def coords(object):
    x, y = c.coords(object['up'])
    return (int(x // block_width), int(y // block_height))

def get_bullet(x, y, direction):
    if direction == 'left':
        # выбираем точку на 10 пикселей левее границы клетки с танком
        # по высоте - середина блока
        rx = block_width * x - 10
        ry = block_height * y + block_height // 2
    elif direction == 'right':
        # выбираем точку на 10 пикселей правее правой границы клетки с танком
        rx = block_width * (x + 1) + 10
        ry = block_height * y + block_height // 2
    elif direction == 'up':
        # выбираем точку на 10 пикселей выше верхней границы
        rx = block_width * x + block_width // 2
        ry = block_height * y - 10
    else:
        # выбираем точку на 10 пикселей нижней границы
        rx = block_width * x + block_width // 2
        ry = block_height * (y + 1) + 10

    bullet = {
        "direction": 'up',
        "up": c.create_image(rx, ry, image=mine_image_up , state='normal'),
        "down": c.create_image(rx, ry, image=mine_image_down, state='hidden'),
        "left": c.create_image(rx, ry, image=mine_image_left, state='hidden'),
        "right": c.create_image(rx, ry, image=mine_image_right, state='hidden'),
    }
    rotate(bullet, direction)
    return bullet


def loop():
    for bullet in bullets:
        # если пуля в клетке, которая недоступна (стена) - удалить ее
        # иначе - передвинуть на 20 пикселей в направлении ее полета
        if bullet ['direction'] == "up":
            move(bullet, 0, -100)
        if bullet ['direction'] == "down":
            move(bullet, 0, 100)
        if bullet ['direction'] == "right":
            move(bullet, 100, 0)
        if bullet ['direction'] == "left":
            move(bullet, -100, 0)
    c.after(50, loop)


#координаты игрока
x = 6
y = 6

#создаем игрока
player_up = c.create_image(x * block_width, y * block_height, image=player_image_up, anchor=NW)
player_down = c.create_image(x * block_width, y * block_height, image=player_image_down, anchor=NW)
player_right = c.create_image(x * block_width, y * block_height, image=player_image_right, anchor=NW)
player_left = c.create_image(x * block_width, y * block_height, image=player_image_left, anchor=NW)

c.itemconfigure(player_left, state='normal')
c.itemconfigure(player_right, state='hidden')
c.itemconfigure(player_up, state='hidden')
c.itemconfigure(player_down, state='hidden')

#проверка доступности клетки
def is_available(i, j):
    if i < 0 or i >= 12 or j < 0 or j >= 12:
        return False
    if game_map[i][j] == 1:
        return False
    return True

#нажатие клавиши
def keyDown(key):
    global x, y

    if key.keycode == 38:
        bullet = get_bullet(x ,y , 'up')
        bullets.append(bullet)

    if key.keycode == 37:
        bullet = get_bullet(x ,y , 'left')
        bullets.append(bullet)

    if key.keycode == 39:
        bullet = get_bullet(x ,y , 'right')
        bullets.append(bullet)

    if key.keycode == 40:
        bullet = get_bullet(x ,y , 'down')
        bullets.append(bullet)

    if key.char == 'a':
        c.itemconfigure(player_left, state='normal')
        c.itemconfigure(player_right, state='hidden')
        c.itemconfigure(player_up, state='hidden')
        c.itemconfigure(player_down, state='hidden')

        if is_available(x - 1, y):
            x -= 1
    if key.char == 'd':
        c.itemconfigure(player_right, state='normal')
        c.itemconfigure(player_left, state='hidden')
        c.itemconfigure(player_up, state='hidden')
        c.itemconfigure(player_down, state='hidden')

        if is_available(x + 1, y):
            x += 1
    if key.char == 'w':
        c.itemconfigure(player_up, state='normal')
        c.itemconfigure(player_right, state='hidden')
        c.itemconfigure(player_left, state='hidden')
        c.itemconfigure(player_down, state='hidden')

        if is_available(x, y - 1):
            y -= 1
    if key.char == 's':
        c.itemconfigure(player_down, state='normal')
        c.itemconfigure(player_right, state='hidden')
        c.itemconfigure(player_up, state='hidden')
        c.itemconfigure(player_left, state='hidden')

        if is_available(x, y + 1):
            y += 1




    c.coords(player_up, x * block_width, y * block_height)
    c.coords(player_down, x * block_width, y * block_height)
    c.coords(player_left, x * block_width, y * block_height)
    c.coords(player_right, x * block_width, y * block_height)

#при нажатии любой клавишы вызываем keyDown
tk.bind("<KeyPress>", keyDown)

c.after(50, loop)

mainloop()
