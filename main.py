import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Fish_hunter"
PLATFORM_TOP = 60


class Fish_hunter_game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Позиция и скорость кубика
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = 100
        self.player_speed_y = 0  # Скорость по вертикали
        self.player_size = 50

        # Состояние клавиш
        self.left_pressed = False
        self.right_pressed = False

    def on_draw(self):
        self.clear()

        # Рисуем платформу
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.width // 2, 30, self.width, 60),
            arcade.color.BROWN
        )

        # Рисуем куб (игрока)
        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.player_x, self.player_y,
                             self.player_size, self.player_size),
            arcade.color.DARK_BLUE
        )

    def on_update(self, delta_time):
        # Гравитация (всегда тянет вниз)
        self.player_speed_y -= 0.5

        self.player_y += self.player_speed_y

        speed = 5
        if self.left_pressed:
            self.player_x -= speed
        if self.right_pressed:
            self.player_x += speed

        # Если кубик на платформе
        if self.player_y < PLATFORM_TOP + self.player_size // 2:
            self.player_y = PLATFORM_TOP + self.player_size // 2
            self.player_speed_y = 0

        # Не даем кубику уйти за экран
        if self.player_x < self.player_size // 2:
            self.player_x = self.player_size // 2
        if self.player_x > SCREEN_WIDTH - self.player_size // 2:
            self.player_x = SCREEN_WIDTH - self.player_size // 2

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE:
            # Прыгаем только если стоим на платформе
            if self.player_y == PLATFORM_TOP + self.player_size // 2:
                self.player_speed_y = 15  # скорость прыжка

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False


def main():
    window = Fish_hunter_game()
    window.run()


if __name__ == "__main__":
    main()
