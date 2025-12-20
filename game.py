import arcade
from character import Potap

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Fish_hunter"
PLATFORM_TOP = 60

class Fish_hunter_game(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Позиция и скорость кубика
        self.players = arcade.SpriteList()
        self.cat_potap = Potap()
        self.players.append(self.cat_potap)

        self.keys_pressed = set()

        # Состояние клавиш
        self.left_pressed = False
        self.right_pressed = False

    def on_draw(self):
        self.clear()

        # Рисуем платформу


        # Кота Потапа (Игрока)
        self.players.draw()
        self.players.draw_hit_boxes()

    def on_update(self, delta_time):
        self.players[0].update(delta_time, self.keys_pressed)
        # Обновляем анимации игрока
        self.players[0].update_animation()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
            self.cat_potap.dx = 0
