import arcade.key
import pyglet
from arcade.gui import UIFlatButton, UIManager
import sqlite3
from game import FishHunterGame
from constants import *
from styles import *
from functions import *

path_db = get_database_path()

CONTROLS = {
    "move_left": arcade.key.A,
    "move_right": arcade.key.D,
    "jump_low": arcade.key.W,
    "jump_high": arcade.key.SPACE,
    "firework": arcade.key.Q,
    "music": arcade.key.P,
    "debug": arcade.key.T,
}


class FishHunterMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

        button_parameters = [("Играть", self.start_game), ("Посмотреть результаты", self.result_score),
                             ("Управление", self.keyboard), ("Настройки", self.setting),
                             ("Выход", self.quit_game)]

        for i in range(5):
            button = UIFlatButton(
                text=button_parameters[i][0],
                width=300,
                style=STYLE
            )
            button.on_click = button_parameters[i][1]
            self.ui_manager.add(button)
            button.center_x = SCREEN_WIDTH // 2
            button.center_y = SCREEN_HEIGHT // 2 - i * 50

    def on_show_view(self):
        # Активируем менеджер UI
        self.ui_manager.enable()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_hide_view(self):
        # Деактивируем менеджер UI
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()
        # Рисуем все элементы
        arcade.draw_text("Fish hunter", 330, 500, arcade.color.BLACK_OLIVE, 24)
        self.ui_manager.draw()

    def start_game(self, event):
        # Вызываем экран с игрой
        self.window.show_view(FishHunterGame(CONTROLS))

    def result_score(self, event):
        # Вызываем экран с результатами
        self.window.show_view(ShowResults())

    def setting(self, event):
        self.window.show_view(Setting())

    def keyboard(self, event):
        self.window.show_view(Keyboard())

    def quit_game(self, event):
        arcade.exit()


class ShowResults(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

        self.conn = sqlite3.connect(path_db)
        self.cursor = self.conn.cursor()
        self.data = self.cursor.execute("SELECT result FROM results").fetchall()
        self.data.sort(key=lambda row: row[0], reverse=True)

        # Для скроллинга
        self.scroll_y = 0
        self.row_height = 30

        menu_button = UIFlatButton(text="Обратно в меню", width=300, style=STYLE)
        menu_button.on_click = self.menu
        self.ui_manager.add(menu_button)
        menu_button.center_x = 400
        menu_button.center_y = 480

    def on_show_view(self):
        # Активируем менеджер UI
        self.ui_manager.enable()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()

        arcade.draw_text("Рекорды",
                         400, 550,
                         arcade.color.BLACK_OLIVE, 24,
                         anchor_x="center", bold=True)

        arcade.draw_text("Лучшие результаты",
                         400, 410,
                         arcade.color.BLACK_OLIVE, 24,
                         anchor_x="center", bold=True)

        # Отрисовка данных
        start_y = 370 - self.scroll_y

        for row_index, row in enumerate(self.data):
            y = start_y - row_index * self.row_height
            arcade.draw_line(0, y + 23, 800, y + 23, arcade.color.BLACK_OLIVE, 3)
            arcade.draw_text(str(row[0]),
                             370, y,
                             arcade.color.BLACK_OLIVE, 16)

    def on_update(self, delta_time):
        pass

    def menu(self, event):
        # Вызываем экран с меню
        self.window.show_view(FishHunterMenu())


class Keyboard(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

        self.row_height = 30

        self.text = [f'{pyglet.window.key.symbol_string(CONTROLS["move_left"])} - Налево',
                     f'{pyglet.window.key.symbol_string(CONTROLS["move_right"])} - Направо',
                     f'{pyglet.window.key.symbol_string(CONTROLS["jump_low"])} - Низкий прыжок',
                     f'{pyglet.window.key.symbol_string(CONTROLS["jump_high"])} - Высокий прыжок',
                     f'{pyglet.window.key.symbol_string(CONTROLS["firework"])} - создать фейерверк',
                     f'{pyglet.window.key.symbol_string(CONTROLS["music"])} - Включить или выключить музыку']

        menu_button = UIFlatButton(text="Обратно в меню", width=300, style=STYLE)
        menu_button.on_click = self.menu
        self.ui_manager.add(menu_button)
        menu_button.center_x = 400
        menu_button.center_y = 480

    def on_show_view(self):
        # Активируем менеджер UI
        self.ui_manager.enable()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()

        for row_index, row in enumerate(self.text):
            y = 370 - row_index * self.row_height
            arcade.draw_text(row,
                             400, y,
                             arcade.color.BLACK_OLIVE, 24,
                             anchor_x="center", bold=True)

    def on_update(self, delta_time):
        pass

    def menu(self, event):
        # Вызываем экран с меню
        self.window.show_view(FishHunterMenu())


class Setting(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

        menu_button = UIFlatButton(text="Обратно в меню", width=300, style=STYLE)
        menu_button.on_click = self.menu
        self.ui_manager.add(menu_button)
        menu_button.center_x = 400
        menu_button.center_y = 480

        button_parameters = [("Идти налево", self.move_left), ("Идти направо", self.move_right),
                             ("Низкий прыжок", self.jump_low), ("Высокий прыжок", self.jump_high),
                             ("Фейерверк", self.firework), ("Включить или выключить музыку", self.music)]

        for i in range(6):
            button = UIFlatButton(
                text=button_parameters[i][0],
                width=300,
                style=STYLE
            )
            button.on_click = button_parameters[i][1]
            self.ui_manager.add(button)
            button.center_x = 600
            button.center_y = 350 - i * 50

        self.check_move_left = False
        self.check_move_right = False
        self.check_jump_low = False
        self.check_jump_high = False
        self.check_firework = False
        self.check_music = False

        self.key_error = False

    def on_show_view(self):
        # Активируем менеджер UI
        self.ui_manager.enable()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

    def on_draw(self):
        self.clear()
        self.ui_manager.draw()
        arcade.draw_text("Изменить управление",
                         600, 400,
                         arcade.color.BLACK_OLIVE, 14,
                         anchor_x="center", bold=True)

        if self.check_move_right or self.check_move_left or self.check_jump_low or self.check_jump_high\
                or self.check_firework or self.check_music:
            arcade.draw_text("Пожалуйста, нажмите на кнопку, на которую хотите поменять управление",
                             400, 30,
                             arcade.color.BLACK_OLIVE, 14,
                             anchor_x="center", bold=True)
        elif self.key_error:
            arcade.draw_text("Эта кнопка уже занята",
                             400, 30,
                             arcade.color.BLACK_OLIVE, 14,
                             anchor_x="center", bold=True)

    def on_update(self, delta_time):
        pass

    def all_false(self):
        self.check_move_left = False
        self.check_move_right = False
        self.check_jump_low = False
        self.check_jump_high = False
        self.check_firework = False
        self.check_music = False

    def move_left(self, event):
        self.all_false()
        self.check_move_left = True

    def move_right(self, event):
        self.all_false()
        self.check_move_right = True

    def jump_low(self, event):
        self.all_false()
        self.check_jump_low = True

    def jump_high(self, event):
        self.all_false()
        self.check_jump_high = True

    def firework(self, event):
        self.all_false()
        self.check_firework = True

    def music(self, event):
        self.all_false()
        self.check_music = True

    def on_key_press(self, key, modifiers):
        if not(key in CONTROLS.values()):
            if self.check_move_left:
                CONTROLS["move_left"] = key
            elif self.check_move_right:
                CONTROLS["move_right"] = key
            elif self.check_jump_low:
                CONTROLS["jump_low"] = key
            elif self.check_jump_high:
                CONTROLS["jump_high"] = key
            elif self.check_firework:
                CONTROLS["firework"] = key
            elif self.check_music:
                CONTROLS["music"] = key
            self.key_error = False
        else:
            self.key_error = True
        self.all_false()

    def menu(self, event):
        # Вызываем экран с меню
        self.window.show_view(FishHunterMenu())
