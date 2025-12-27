import arcade
from character import Potap, SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORM_TOP


class Fish_hunter_game(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Создаем игрока
        self.all_sprite = arcade.SpriteList()
        self.player = Potap()
        self.all_sprite.append(self.player)

        # Управление
        self.left_pressed = False
        self.right_pressed = False

    def on_draw(self):
        self.clear()

        # Рисуем платформу
        arcade.draw_rect_filled(
            arcade.rect.XYWH(SCREEN_WIDTH // 2, PLATFORM_TOP // 2,
                             SCREEN_WIDTH, PLATFORM_TOP),
            arcade.color.BROWN
        )

        # Рисуем игрока
        self.all_sprite.draw()

    def on_update(self, delta_time):
        # Обновляем движение
        if self.left_pressed and not self.right_pressed:
            self.player.move_left()
        elif self.right_pressed and not self.left_pressed:
            self.player.move_right()
        else:
            self.player.stop_horizontal()

        # Обновляем физику и движение
        self.player.update_movement()

        # Обновляем анимацию
        self.player.update_animation(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            self.player.jump()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
