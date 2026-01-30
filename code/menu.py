import arcade.key
import pyglet
import json
from arcade.gui import UIFlatButton, UIManager
import sqlite3
from game import FishHunterGame, path_db, path_settings
from constants import *
from styles import *

with open(path_settings, 'r', encoding='utf-8') as f:
    setting = f.read()
controls = json.loads(setting)


class FishHunterMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

        self.background_color = (25, 55, 95)

        button_parameters = [
            ("Играть", self.start_game),
            ("Результаты", self.result_score),
            ("Настройки", self.setting),
            ("Выход", self.quit_game)
        ]

        for i in range(4):
            button = UIFlatButton(
                text=button_parameters[i][0],
                width=350,
                height=50,
                style=STYLE
            )
            button.on_click = button_parameters[i][1]
            self.ui_manager.add(button)
            button.center_x = SCREEN_WIDTH // 2
            button.center_y = SCREEN_HEIGHT // 2 - i * 60 + 40

    def on_show_view(self):
        self.ui_manager.enable()
        arcade.set_background_color(self.background_color)

    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()

        arcade.set_background_color(self.background_color)

        arcade.draw_text(
            "Fish Hunter",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            (255, 215, 0),
            36,
            anchor_x="center",
            bold=True,
            font_name=("calibri", "arial")
        )

        self.ui_manager.draw()

    def start_game(self, event):
        self.window.show_view(FishHunterGame(controls, self))

    def result_score(self, event):
        self.window.show_view(ShowResults())

    def setting(self, event):
        self.window.show_view(Setting())

    def quit_game(self, event):
        arcade.exit()


class ShowResults(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

        # Открываем базу данных
        self.conn = sqlite3.connect(path_db)
        self.cursor = self.conn.cursor()
        self.data = self.cursor.execute("SELECT result FROM results").fetchall()
        self.data.sort(key=lambda row: row[0], reverse=True)

        self.scroll_y = 0
        self.row_height = 35

        menu_button = UIFlatButton(
            text="← Назад в меню",
            width=250,
            height=45,
            style=INFO_BUTTON_STYLE
        )
        menu_button.on_click = self.menu
        self.ui_manager.add(menu_button)
        menu_button.center_x = 400
        menu_button.center_y = 530

    def on_show_view(self):
        self.ui_manager.enable()
        arcade.set_background_color((40, 80, 140))

    def on_draw(self):
        self.clear()

        arcade.set_background_color((40, 80, 140))

        self.ui_manager.draw()

        arcade.draw_text(
            "Таблица рекордов",
            400, 470,
            (255, 215, 0),
            28,
            anchor_x="center",
            bold=True,
            font_name=("calibri", "arial")
        )

        arcade.draw_text(
            "Лучшие результаты игроков",
            400, 430,
            (200, 220, 255),
            18,
            anchor_x="center",
            font_name=("calibri", "arial")
        )

        # Рамка для таблицы
        arcade.draw_line(150, 420, 650, 420, (100, 149, 237), 3)
        arcade.draw_line(650, 420, 650, 80, (100, 149, 237), 3)
        arcade.draw_line(150, 80, 650, 80, (100, 149, 237), 3)
        arcade.draw_line(150, 420, 150, 80, (100, 149, 237), 3)

        # Заголовок таблицы
        arcade.draw_text(
            "Место",
            275, 395,
            (100, 149, 237),
            18,
            anchor_x="center",
            bold=True
        )

        arcade.draw_text(
            "Счет",
            525, 395,
            (100, 149, 237),
            18,
            anchor_x="center",
            bold=True
        )

        # Разделительная линия заголовка
        arcade.draw_line(150, 380, 650, 380, (100, 149, 237), 2)

        start_y = 350 - self.scroll_y

        for row_index, row in enumerate(self.data[:10]):
            y = start_y - row_index * self.row_height
            arcade.draw_text(
                f"{row_index + 1}.",
                275, y,
                arcade.color.WHITE,
                20,
                anchor_x="center"
            )

            arcade.draw_text(
                str(row[0]),
                525, y,  #
                arcade.color.WHITE,
                22,
                anchor_x="center",
                bold=True
            )

            # Разделительная линия между строками
            arcade.draw_line(150, y - 20, 650, y - 20, (100, 149, 237, 100), 1)

    def menu(self, event):
        self.window.show_view(FishHunterMenu())


class Setting(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

        self.row_height = 55

        menu_button = UIFlatButton(
            text="← Назад в меню",
            width=250,
            height=45,
            style=INFO_BUTTON_STYLE
        )
        menu_button.on_click = self.menu
        self.ui_manager.add(menu_button)
        menu_button.center_x = 400
        menu_button.center_y = 550

        self.text_1 = [
            f'{pyglet.window.key.symbol_string(controls["move_left"])}',
            f'{pyglet.window.key.symbol_string(controls["move_right"])}',
            f'{pyglet.window.key.symbol_string(controls["jump_low"])}',
            f'{pyglet.window.key.symbol_string(controls["jump_high"])}'
        ]

        self.text_2 = [
            f'{pyglet.window.key.symbol_string(controls["firework"])}',
            f'{pyglet.window.key.symbol_string(controls["music"])}',
            f'{pyglet.window.key.symbol_string(controls["exit"])}'
        ]

        button_parameters = [
            ("Идти налево", self.move_left),
            ("Идти направо", self.move_right),
            ("Низкий прыжок", self.jump_low),
            ("Высокий прыжок", self.jump_high),
            ("Фейерверк", self.firework),
            ("Музыка", self.music),
            ("Выход в меню", self.exit)
        ]

        for i in range(4):
            button = UIFlatButton(
                text=button_parameters[i][0],
                width=290,
                height=45,
                style=INFO_BUTTON_STYLE
            )
            button.on_click = button_parameters[i][1]
            self.ui_manager.add(button)
            button.center_x = 175
            button.center_y = 380 - i * 55

        for i in range(4, 7):
            button = UIFlatButton(
                text=button_parameters[i][0],
                width=290,
                height=45,
                style=INFO_BUTTON_STYLE
            )
            button.on_click = button_parameters[i][1]
            self.ui_manager.add(button)
            button.center_x = 560
            button.center_y = 380 - (i - 4) * 55

        self.check_move_left = False
        self.check_move_right = False
        self.check_jump_low = False
        self.check_jump_high = False
        self.check_firework = False
        self.check_music = False
        self.check_exit = False

        self.key_error = False
        self.success_message = False
        self.success_timer = 0

    def on_show_view(self):
        self.ui_manager.enable()
        arcade.set_background_color((60, 100, 160))

    def on_draw(self):
        self.clear()

        # Цветной фон
        arcade.set_background_color((60, 100, 160))

        self.ui_manager.draw()

        arcade.draw_text(
            "Настройка управления",
            400, 470,
            (255, 215, 0),
            28,
            anchor_x="center",
            bold=True,
            font_name=("calibri", "arial")
        )

        arcade.draw_text(
            "Нажмите на действие, которое хотите изменить,",
            400, 440,
            arcade.color.LIGHT_BLUE,
            16,
            anchor_x="center",
            font_name=("calibri", "arial")
        )

        arcade.draw_text(
            "затем нажмите новую клавишу на клавиатуре",
            400, 420,
            arcade.color.LIGHT_BLUE,
            16,
            anchor_x="center",
            font_name=("calibri", "arial")
        )

        # Списки управления
        for row_index, row in enumerate(self.text_1):
            y = 370 - row_index * self.row_height
            color = (255, 255, 255) if row_index < 6 else (255, 200, 200)

            arcade.draw_text(
                row,
                375, y,
                color,
                18,
                anchor_x="center",
                font_name=("calibri", "arial")
            )
        for row_index, row in enumerate(self.text_2):
            y = 370 - row_index * self.row_height
            color = (255, 255, 255) if row_index < 6 else (255, 200, 200)

            arcade.draw_text(
                row,
                760, y,
                color,
                18,
                anchor_x="center",
                font_name=("calibri", "arial")
            )

        # Сообщения
        if self.check_move_right or self.check_move_left or self.check_jump_low or self.check_jump_high \
                or self.check_firework or self.check_music or self.check_exit:
            arcade.draw_text(
                "Нажмите новую клавишу на клавиатуре",
                400, 50,
                (100, 255, 100),
                18,
                anchor_x="center",
                bold=True,
                font_name=("calibri", "arial")
            )
        elif self.key_error:
            arcade.draw_text(
                "Эта клавиша уже занята!",
                400, 50,
                (255, 100, 100),
                18,
                anchor_x="center",
                bold=True,
                font_name=("calibri", "arial")
            )
        elif self.success_message:
            arcade.draw_text(
                "Управление успешно изменено!",
                400, 50,
                (100, 255, 100),
                18,
                anchor_x="center",
                bold=True,
                font_name=("calibri", "arial")
            )

    def on_update(self, delta_time):
        if self.success_message:
            self.success_timer += delta_time
            if self.success_timer > 2:
                self.success_message = False
                self.success_timer = 0

    def all_false(self):
        self.check_move_left = False
        self.check_move_right = False
        self.check_jump_low = False
        self.check_jump_high = False
        self.check_firework = False
        self.check_music = False
        self.check_exit = False

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

    def exit(self, event):
        self.all_false()
        self.check_exit = True

    def on_key_press(self, key, modifiers):
        if not (key in controls.values()):
            if self.check_move_left:
                controls["move_left"] = key
            elif self.check_move_right:
                controls["move_right"] = key
            elif self.check_jump_low:
                controls["jump_low"] = key
            elif self.check_jump_high:
                controls["jump_high"] = key
            elif self.check_firework:
                controls["firework"] = key
            elif self.check_music:
                controls["music"] = key
            elif self.check_exit:
                controls["exit"] = key

            self.key_error = False
            self.success_message = True
            self.success_timer = 0
        else:
            self.key_error = True
            self.success_message = False
        self.all_false()
        self.text_1 = [
            f'{pyglet.window.key.symbol_string(controls["move_left"])}',
            f'{pyglet.window.key.symbol_string(controls["move_right"])}',
            f'{pyglet.window.key.symbol_string(controls["jump_low"])}',
            f'{pyglet.window.key.symbol_string(controls["jump_high"])}'
        ]

        self.text_2 = [
            f'{pyglet.window.key.symbol_string(controls["firework"])}',
            f'{pyglet.window.key.symbol_string(controls["music"])}',
            f'{pyglet.window.key.symbol_string(controls["exit"])}'
        ]

    def menu(self, event):
        with open(path_settings, 'w') as f:
            json.dump(controls, f)
        self.window.show_view(FishHunterMenu())
