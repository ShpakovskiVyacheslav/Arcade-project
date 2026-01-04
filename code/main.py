import arcade
from arcade.gui import UIFlatButton, UIManager
from game import FishHunterGame
from constants import *


class FishHunterMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_manager = UIManager()

        style = {
            "normal": {
                "font_name": ("calibri", "arial"),
                "font_size": 15,
                "font_color": arcade.color.BLACK_OLIVE,
                "bg": arcade.color.LIGHT_BLUE,
                "border": arcade.color.BLACK_OLIVE,
                "border_width": 2
            },
            "hover": {"font_name": ("calibri", "arial"),
                      "font_size": 15,
                      "font_color": arcade.color.LIGHT_BLUE,
                      "bg": arcade.color.BLACK_OLIVE,
                      "border": arcade.color.BLACK_OLIVE,
                      "border_width": 2},
            "press": {"font_name": ("calibri", "arial"),
                      "font_size": 15,
                      "font_color": arcade.color.LIGHT_BLUE,
                      "bg": arcade.color.BLACK_OLIVE,
                      "border": arcade.color.BLACK_OLIVE,
                      "border_width": 2}
        }

        # Создаем кнопку "Играть"
        play_button = UIFlatButton(text="Играть", width=300, style=style)
        play_button.on_click = self.start_game
        self.ui_manager.add(play_button)
        play_button.center_x = SCREEN_WIDTH // 2
        play_button.center_y = SCREEN_HEIGHT // 2

        # Создаем кнопку "Выход"
        quit_button = UIFlatButton(text="Выход", width=300, style=style)
        quit_button.on_click = self.quit_game
        self.ui_manager.add(quit_button)
        quit_button.center_x = SCREEN_WIDTH // 2
        quit_button.center_y = SCREEN_HEIGHT // 2 - 50

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

    def quit_game(self, event):
        arcade.exit()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = FishHunterMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
