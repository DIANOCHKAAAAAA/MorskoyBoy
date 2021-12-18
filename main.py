"""
Программа «Морской бой».
«Морской бой» — игра, в которой игрок и компьютер по очереди нажимают на клетки неизвестной им карте соперника.
Если у соперника по этим координатам имеется корабль, то корабль или его часть «топится».
Цель игрока — первым потопить все корабли противника.
"""


from tkinter import *
import time
import random


def draw_table(offset=0):
    """
    Рисует игровое поле

    Args:
        offset (int): Смещение поля на холсте по координате x
    """

    global canvas
    for i in range(field_size['x'] + 1):
        canvas.create_line(offset + step['x'] * i, 0, offset + step['x'] * i, canvas_size['y'])
    for i in range(field_size['y'] + 1):
        canvas.create_line(offset, step['y'] * i, offset + canvas_size['x'], step['y'] * i)


def change_current_label(player_label, computer_label, current_label):
    """
    Изменяет параметры надписей

    Args:
        player_label (Label): Надпись игрока
        computer_label (Label): Надпись компьютера
        current_label (Label): Надпись о текущем ходе

    Raises:
        TypeError: Если хотя бы один переданный аргумент равен None
    """

    if player_label is None or computer_label is None or current_label is None:
        raise TypeError('Labels are undefined')
    else:
        if player_turn:
            player_label.configure(bg='lightgreen')
            computer_label.configure(bg='#f0f0f0')
            current_label.configure(text='Ходит компьютер')
        else:
            computer_label.configure(bg='lightgreen')
            player_label.configure(bg='#f0f0f0')
            current_label.configure(text='Ходите Вы')
        current_label.place(x=canvas_size['x'] + menu['x'] // 2 - current_label.winfo_reqwidth() // 2,
                            y=canvas_size['y'])


def show_player_ships():
    """
    Показывает корабли игрока
    """

    global canvas_objects
    for i in range(field_size['x']):
        for j in range(field_size['y']):
            if player_ships[j][i] > 0:
                color = 'green'
                if computer_clicks[j][i] != -1:
                    color = 'red'
                rectangle = canvas.create_rectangle(i * step['x'], j * step['y'], (i + 1) * step['x'],
                                                    (j + 1) * step['y'], fill=color)
                canvas_objects.append(rectangle)


def show_computer_ships():
    """
    Показывает корабли компьютера.
    """

    global canvas_objects
    for i in range(field_size['x']):
        for j in range(field_size['y']):
            if computer_ships[j][i] > 0:
                color = 'red'
                if player_clicks[j][i] != -1:
                    color = 'green'
                rectangle = canvas.create_rectangle(canvas_size['x'] + menu['x'] + i * step['x'], j * step['y'],
                                                    canvas_size['x'] + menu['x'] + (i + 1) * step['x'],
                                                    (j + 1) * step['y'], fill=color)
                canvas_objects.append(rectangle)


def generate_ships(size):
    """
    Генерирует поле заданного размера с расставленными на нём кораблями

    Args:
        size (dict): Размеры поля.
            Словарь, ключами которого являются названия осей (x и y), а значениями - количество клеток по заданной оси
        computer_label (Label): Надпись компьютера
        current_label (Label): Надпись о текущем ходе

    Returns:
        list[list[int]]: Сгенерированное поле

    Raises:
        ValueError: Если размеры поля не имеют возможности вместить в себя все корабли из классической игры
    """

    if size['x'] * size['y'] < 100 or size['x'] < 4 or size['y'] < 4:
        raise ValueError('Wrong field size')

    ships = [[0 for i in range(size['x'])] for j in range(size['y'])]
    field = [[0 for i in range(-1, size['x'] + 1)] for j in range(-1, size['y'] + 1)]

    for ship in ships_list:
        able_to_add = False
        while not able_to_add:
            x = random.randrange(size['x'])
            y = random.randrange(size['y'])
            direction = random.choice([{'dx': 1, 'dy': 0}, {'dx': 0, 'dy': 1}, {'dx': -1, 'dy': 0}, {'dx': 0, 'dy': -1}])
            up_left_angle = {'x': 0, 'y': 0}
            down_right_angle = {'x': 0, 'y': 0}
            if direction['dx'] == 1 and direction['dy'] == 0:
                up_left_angle = {'x': x - 1, 'y': y - 1}
                down_right_angle = {'x': x + ship, 'y': y + 1}
            elif direction['dx'] == -1 and direction['dy'] == 0:
                up_left_angle = {'x': x - ship, 'y': y - 1}
                down_right_angle = {'x': x + 1, 'y': y + 1}
            elif direction['dx'] == 0 and direction['dy'] == 1:
                up_left_angle = {'x': x - 1, 'y': y - 1}
                down_right_angle = {'x': x + 1, 'y': y + ship}
            else:
                up_left_angle = {'x': x - 1, 'y': y - ship}
                down_right_angle = {'x': x + 1, 'y': y + 1}
            if up_left_angle['x'] < -1 or up_left_angle['y'] < -1 or down_right_angle['x'] > size['x'] or down_right_angle['y'] > size['y']:
                continue
            able_to_add = True
            xo = up_left_angle['x']
            yo = up_left_angle['y']
            while True:
                if field[yo + 1][xo + 1] != 0:
                    able_to_add = False
                    break
                if xo == down_right_angle['x'] and yo == down_right_angle['y']:
                    # for j in range(len(ships)):
                    #     for i in range(len(ships[j])):
                    #         print(' ' + str(ships[j][i]), end = '')
                    #     print()
                    # print()
                    for delta in range(ship):
                        field[y + 1 + delta * direction['dy']][x + 1 + delta * direction['dx']] = 1
                        ships[y + delta * direction['dy']][x + delta * direction['dx']] = 1
                    break
                if xo == down_right_angle['x']:
                    yo += 1
                    xo = up_left_angle['x']
                else:
                    xo += 1
    return ships


def begin_again():
    """
    Начинает игру сначала
    """

    global canvas_objects, player_ships, computer_ships, player_clicks, computer_clicks, boom
    for element in canvas_objects:
        canvas.delete(element)
    canvas_objects = []
    player_ships = generate_ships(field_size)
    computer_ships = generate_ships(field_size)
    player_clicks = [[-1 for i in range(field_size['x'])] for j in range(field_size['y'])]
    computer_clicks = [[-1 for i in range(field_size['x'])] for j in range(field_size['y'])]
    boom = [[0 for i in range(field_size['x'])] for j in range(field_size['y'])]


def draw_point(x, y, ships, offset=0):
    """
    Рисует точку, указывающую место, в которое был произведён выстрел

    Args:
        x (int): Координата x выстрела
        y (int): Координата y выстрела
        ships (list[list[int]]): Карта расположения кораблей
        offset (int): Смещение поля на холсте по координате x
    """

    global canvas_objects
    if ships[y][x] == 0:
        point = canvas.create_oval(x * step['x'] + offset, y * step['y'], (x + 1) * step['x'] + offset,
                                   (y + 1) * step['y'], fill='blue')
        canvas_objects.append(point)
    if ships[y][x] > 0:
        point = canvas.create_oval(x * step['x'] + offset, y * step['y'], (x + 1) * step['x'] + offset,
                                   (y + 1) * step['y'], fill='pink')
        canvas_objects.append(point)


def check_winner(size, ships, clicks):
    """
    Проверяет победил ли кто-либо из игроков

    Args:
        size (dict): Размеры поля.
            Словарь, ключами которого являются названия осей (x и y), а значениями - количество клеток по заданной оси
        ships (list[list[int]]): Карта расположения кораблей
        clicks (list[list[int]]): Список нажатий на карту

    Returns:
        bool: True, если все корабли соперника «потоплены»
    """

    win = True
    for i in range(size['x']):
        for j in range(size['y']):
            if ships[j][i] > 0:
                if clicks[j][i] == -1:
                    win = False
                    break
    return win


def computer_turn():
    """
    Ход компьютера
    """

    global window
    global player_turn
    global player_clicks, computer_clicks

    window.update()
    time.sleep(1)
    player_turn = False
    if not computer_vision:
        ip_x = random.randrange(0, field_size['x'])
        ip_y = random.randrange(0, field_size['y'])
        while not player_clicks[ip_y][ip_x] == -1:
            ip_x = random.randrange(0, field_size['x'])
            ip_y = random.randrange(0, field_size['y'])
    else:
        ip_x = random.randrange(0, field_size['x'])
        ip_y = random.randrange(0, field_size['y'])
        # some code
    player_clicks[ip_y][ip_x] = 7
    draw_point(ip_x, ip_y, player_ships )
    if check_winner(field_size, player_ships, player_clicks):
        winner = 'Вы проиграли'
        print(winner)
        player_clicks = [[10 for i in range(field_size['x'])] for i in range(field_size['y'])]
        computer_clicks = [[10 for i in range(field_size['x'])] for i in range(field_size['y'])]
        outer_rect = canvas.create_rectangle(step['x'] * 3, step['y'] * 3,
                                             2 * canvas_size['x'] + menu['x'] - step['x'] * 3,
                                             canvas_size['y'] - step['y'], fill='#00FA9A')
        canvas_objects.append(outer_rect)
        inner_rect = canvas.create_rectangle(step['x'] * 3 + step['x'] // 2, step['y'] * 3 + step['y'] // 2,
                                             2 * canvas_size['x'] + menu['x'] - step['x'] * 3 - step['x'] // 2,
                                             canvas_size['y'] - step['y'] - step['y'] // 2, fill='#20B2AA')
        canvas_objects.append(inner_rect)
        text = canvas.create_text(step['x'] * 10, step['y'] * 5, text=winner, font=('Arial', 50), justify=CENTER)
        canvas_objects.append(text)


def add_to_all(event):
    """
    Ход игрока.
        https://github.com/WISEPLAT/python-code.git

    Args:
        event ({num}): Событие (нажатие на кнопку мыши)
    """

    global player_turn
    global player_ships, computer_ships
    global player_clicks, computer_clicks

    mouse_button = 0  # ЛКМ
    if event.num == 3:
        mouse_button = 1  # ПКМ
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    ip_x = mouse_x // step['x']
    ip_y = mouse_y // step['y']
    # первое игровое поле
    if ip_x < field_size['x'] and ip_y < field_size['y'] and player_turn:
        if player_clicks[ip_y][ip_x] == -1:
            player_clicks[ip_y][ip_x] = mouse_button
            if computer_ships[ip_y][ip_x] == 0:
                player_turn = False
            draw_point(ip_x, ip_y, player_ships)
            if check_winner(field_size, player_ships, player_clicks):
                player_turn = True
                winner = 'Вы проиграли'
                print(winner)
                player_clicks = [[10 for i in range(field_size['x'])] for j in range(field_size['y'])]
                computer_clicks = [[10 for i in range(field_size['x'])] for j in range(field_size['y'])]
                outer_rect = canvas.create_rectangle(step['x'] * 3, step['y'] * 3,
                                                     2 * canvas_size['x'] + menu['x'] - step['x'] * 3,
                                                     canvas_size['y'] - step['y'], fill='#00FA9A')
                canvas_objects.append(outer_rect)
                inner_rect = canvas.create_rectangle(step['x'] * 3 + step['x'] // 2, step['y'] * 3 + step['y'] // 2,
                                                     2 * canvas_size['x'] + menu['x'] - step['x'] * 3 - step['x'] // 2,
                                                     canvas_size['y'] - step['y'] - step['y'] // 2, fill='#20B2AA')
                canvas_objects.append(inner_rect)
                text = canvas.create_text(step['x'] * 10, step['y'] * 5, text=winner, font=('Arial', 50), justify=CENTER)
                canvas_objects.append(text)
    # второе игровое поле
    if ip_x >= field_size['x'] + 4 and ip_x <= 2 * field_size['x'] + 4 and ip_y < field_size['y'] and not player_turn:
        if computer_clicks[ip_y][ip_x - field_size['x'] - 4] == -1:
            computer_clicks[ip_y][ip_x - field_size['x'] - 4] = mouse_button
            player_turn = True
            draw_point(ip_x - field_size['x'] - 4, ip_y, computer_ships, canvas_size['x'] + menu['x'])
            if check_winner(field_size, computer_ships, computer_clicks):
                player_turn = False
                winner = 'Вы победили!!!'
                print(winner)
                player_clicks = [[10 for i in range(field_size['x'])] for j in range(field_size['y'])]
                computer_clicks = [[10 for i in range(field_size['x'])] for j in range(field_size['y'])]
                outer_rect = canvas.create_rectangle(step['x'] * 3, step['y'] * 3,
                                                     2 * canvas_size['x'] + menu['x'] - step['x'] * 3,
                                                     canvas_size['y'] - step['y'], fill='#00FA9A')
                canvas_objects.append(outer_rect)
                inner_rect = canvas.create_rectangle(step['x'] * 3 + step['x'] // 2, step['y'] * 3 + step['y'] // 2,
                                                     2 * canvas_size['x'] + menu['x'] - step['x'] * 3 - step['x'] // 2,
                                                     canvas_size['y'] - step['y'] - step['y'] // 2, fill='#20B2AA')
                canvas_objects.append(inner_rect)
                text = canvas.create_text(step['x'] * 10, step['y'] * 5, text=winner, font=('Arial', 50), justify=CENTER)
                canvas_objects.append(text)
            else:
                change_current_label(player_label, computer_label, current_label)
                computer_turn()
    change_current_label(player_label, computer_label, current_label)


def main():
    """
    Главная функция. Запускает игру
    """

    global player_ships, computer_ships
    global canvas_objects
    global player_clicks, computer_clicks
    global boom
    global player_turn
    global computer_vision
    global player_label, computer_label, current_label

    app_running = True
    player_ships = [[0 for i in range(field_size['x'])] for i in range(field_size['y'])]
    computer_ships = [[0 for i in range(field_size['x'])] for i in range(field_size['y'])]
    canvas_objects = []
    player_clicks = [[-1 for i in range(field_size['x'])] for i in range(field_size['y'])]
    computer_clicks = [[-1 for i in range(field_size['x'])] for i in range(field_size['y'])]
    boom = [[0 for i in range(field_size['x'])] for i in range(field_size['y'])]
    player_turn = False
    computer_vision = False

    window.title('Морской Бой')
    window.resizable(0, 0)
    window.wm_attributes('-topmost', 1)
    canvas.create_rectangle(0, 0, canvas_size['x'], canvas_size['y'], fill='lightblue')
    canvas.create_rectangle(canvas_size['x'] + menu['x'], 0, 2 * canvas_size['x'] + menu['x'], canvas_size['y'], fill='lightblue')
    canvas.pack()
    window.update()

    draw_table()
    draw_table(canvas_size['x'] + menu['x'])

    player_label = Label(window, text='Вы', font=('Helvetica', 16))
    player_label.place(x=canvas_size['x'] // 2 - player_label.winfo_reqwidth() // 2, y=canvas_size['y'] + 3)
    computer_label = Label(window, text='Компьютер', font=('Helvetica', 16))
    computer_label.place(x=canvas_size['x'] + menu['x'] + canvas_size['x'] // 2 - computer_label.winfo_reqwidth() // 2, y=canvas_size['y'] + 3)
    player_label.configure(bg='red')
    player_label.configure(bg='#f0f0f0')
    current_label = Label(window, text='@@@@@@@', font=('Helvetica', 16))
    current_label.place(x=canvas_size['x'] + menu['x'] // 2 - current_label.winfo_reqwidth() // 2, y=canvas_size['y'])
    change_current_label(player_label, computer_label, current_label)

    btn_show_player_ships = Button(window, text='Показать мое поле', command=show_player_ships)
    btn_show_player_ships.place(x=canvas_size['x'] + 20, y=30)
    btn_show_computer_ships = Button(window, text='Показать поле компьютера', command=show_computer_ships)
    btn_show_computer_ships.place(x=canvas_size['x'] + 20, y=70)
    btn_begin_again = Button(window, text='Начать заново!', command=begin_again)
    btn_begin_again.place(x=canvas_size['x'] + 20, y=110)

    canvas.bind_all("<Button-1>", add_to_all) # ЛКМ
    canvas.bind_all("<Button-3>", add_to_all) # ПКМ

    player_ships = generate_ships(field_size)
    computer_ships = generate_ships(field_size)

    while app_running:
        if app_running:
            window.update_idletasks()
            window.update()
        time.sleep(0.005)


window = Tk()
canvas_size = {'x': 500, 'y': 500}
field_size = {'x': 10, 'y': 10}
step = {'x': canvas_size['x'] // field_size['x'], 'y': canvas_size['y'] // field_size['y']}
canvas_size['x'] = step['x'] * field_size['x']
canvas_size['y'] = step['y'] * field_size['y']
menu = {'x': step['x'] * 4, 'y': 40}
canvas = Canvas(window, width=2 * canvas_size['x'] + menu['x'], height=canvas_size['y'] + menu['y'], bd=0, highlightthickness=0)

player_ships = []
computer_ships = []
canvas_objects = []
player_clicks = []
computer_clicks = []
boom = []
ships_list = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
player_turn = False
computer_vision = False

player_label = None
computer_label = None
current_label = None

if __name__ == '__main__':
    main()
