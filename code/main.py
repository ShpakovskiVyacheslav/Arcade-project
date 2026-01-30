import arcade
from constants import *
from menu import FishHunterMenu

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = FishHunterMenu()
    window.show_view(menu_view)
    arcade.run()
