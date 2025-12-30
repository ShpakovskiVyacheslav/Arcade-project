import arcade
from character import Player_Potap, SCREEN_WIDTH, SCREEN_HEIGHT, CAMERA_LERP, GRAVITY
from arcade.camera import Camera2D

TILE_SCALING = 1

class Fish_hunter_game(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.world_camera = Camera2D()
        self.gui_camera = Camera2D()

        # Создаем игрока
        self.all_sprite = arcade.SpriteList()
        self.player = Player_Potap()
        self.all_sprite.append(self.player)

        # Управление
        self.left_pressed = False
        self.right_pressed = False

        map_name = "test.tmx"
        self.tile_map = arcade.load_tilemap(f"static/levels/{map_name}", scaling=TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.physics_engine = arcade.PhysicsEnginePlatformer(player_sprite=self.player,
                                                             platforms=self.scene["collision"],
                                                             gravity_constant=GRAVITY)

    def on_draw(self):
        self.clear()
        # камера
        self.world_camera.use()
        self.scene.draw()
        self.all_sprite.draw()
        self.gui_camera.use()

        # Рисуем игрока

    def on_update(self, delta_time):
        # Обновляем движение
        if self.left_pressed and not self.right_pressed:
            self.player.move_left()
        elif self.right_pressed and not self.left_pressed:
            self.player.move_right()
        else:
            self.player.stop_horizontal()

        # Обновляем физику и движение
        self.physics_engine.update()
        self.player.update_movement()

        # Обновляем анимацию
        self.player.update_animation(delta_time)

        tx, ty = self.player.center_x, self.player.center_y
        cx, cy = self.world_camera.position
        smooth = (cx + (tx - cx) * CAMERA_LERP,
                  cy + (ty - cy) * CAMERA_LERP)

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2

        world_w = 4000
        world_h = 4000
        cam_x = max(half_w, min(world_w - half_w, smooth[0]))
        cam_y = max(half_h, min(world_h - half_h, smooth[1]))
        self.world_camera.position = (cam_x, cam_y)
        self.gui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE and self.physics_engine.can_jump(y_distance=1):
            self.player.jump()
            self.physics_engine.jump(15)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
