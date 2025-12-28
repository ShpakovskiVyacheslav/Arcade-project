import arcade
from character import Potap, SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORM_TOP

TILE_SCALING = 1


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

        map_name = "platform.tmx"
        tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)
        self.platform = tile_map.sprite_lists["grass"]

        # c PhysicsEngineSimple работает криво
        # self.physics_engine = arcade.PhysicsEngineSimple(
        #     self.player, self.platform
        # )

    def on_draw(self):
        self.clear()

        self.platform.draw()

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

        # self.physics_engine.update()

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
