import arcade
import sqlite3
from arcade.gui import UIFlatButton, UIManager
from game import FishHunterGame
from constants import *
from styles import *


class FishHunterMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

        button_parameters = [("Играть", self.start_game), ("Посмотреть результаты", self.result_score), ("Управление", self.keyboard),
                             ("Выход", self.quit_game)]

        for i in range(4):
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
        self.window.show_view(FishHunterGame())

    def result_score(self, event):
        # Вызываем экран с результатами
        self.window.show_view(ShowResults())

    def keyboard(self, event):
        self.window.show_view(Keyboard())

    def quit_game(self, event):
        arcade.exit()


class ShowResults(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

        self.conn = sqlite3.connect('../for_database/records.sqlite')
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

        # Для скроллинга
        self.scroll_y = 0
        self.row_height = 30

        self.text = ['A или LEFT - Налево', 'D или RIGHT - Направо', 'W или UP - Низкий прыжок',
                     'Space - Высокий прыжок', 'Q - создать фейерверк', 'P - Включить или выключить музыку']

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


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = FishHunterMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
