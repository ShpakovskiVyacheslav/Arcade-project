import arcade
from arcade.gui import UIFlatButton, UIManager
from character import Player_Potap
from arcade.camera import Camera2D
from constants import *
from enemies import Enemy


class FishHunterGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.world_camera = Camera2D()
        self.gui_camera = Camera2D()

        # UI менеджер для кнопок
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        # Создаем игрока
        self.all_sprite = arcade.SpriteList()
        self.player = Player_Potap()
        self.all_sprite.append(self.player)

        # Создаем список врагов
        self.enemies_sprites = arcade.SpriteList()

        # Управление
        self.left_pressed = False
        self.right_pressed = False

        self.level = 1
        self.tile_map = arcade.load_tilemap(f"../static/levels/level{self.level}.tmx", scaling=TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # создаем врагов
        for i in self.scene["enemies"]:
            enemy = Enemy(self.scene["earth"])
            enemy.position = i.position
            self.enemies_sprites.append(enemy)
            self.all_sprite.append(enemy)
        self.score = 0

        # Кнопки (будут показаны при смерти)
        self.death_buttons = []

        # Стиль для кнопок
        self.button_style = {
            "normal": {
                "font_name": ("calibri", "arial"),
                "font_size": 15,
                "font_color": arcade.color.WHITE,
                "bg": arcade.color.RED,
                "border": arcade.color.DARK_RED,
                "border_width": 2
            },
            "hover": {
                "font_name": ("calibri", "arial"),
                "font_size": 15,
                "font_color": arcade.color.RED,
                "bg": arcade.color.WHITE,
                "border": arcade.color.DARK_RED,
                "border_width": 2
            },
            "press": {
                "font_name": ("calibri", "arial"),
                "font_size": 15,
                "font_color": arcade.color.RED,
                "bg": arcade.color.LIGHT_GRAY,
                "border": arcade.color.DARK_RED,
                "border_width": 2
            }
        }

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.scene["earth"],
            gravity_constant=GRAVITY
        )

        self.music = arcade.load_sound("../static/sounds/background music.mp3")
        self.music_player = arcade.play_sound(self.music, loop=True, volume=VOLUME)
        self.music_enabled = True

        self.cheating = False

    def create_death_buttons(self):
        # Создаем "кнопки смерти"
        # Очищаем старые кнопки
        for button in self.death_buttons:
            self.ui_manager.remove(button)
        self.death_buttons.clear()

        # Кнопка "Начать заново"
        restart_button = UIFlatButton(
            text="Начать заново",
            width=200,
            height=40,
            style=self.button_style
        )
        restart_button.on_click = self.restart_game
        self.ui_manager.add(restart_button)
        restart_button.center_x = SCREEN_WIDTH // 2
        restart_button.center_y = SCREEN_HEIGHT // 2 - 40
        self.death_buttons.append(restart_button)

        # Кнопка "Вернуться в меню"
        menu_button = UIFlatButton(
            text="Вернуться в меню",
            width=200,
            height=40,
            style=self.button_style
        )
        menu_button.on_click = self.return_to_menu
        self.ui_manager.add(menu_button)
        menu_button.center_x = SCREEN_WIDTH // 2
        menu_button.center_y = SCREEN_HEIGHT // 2 - 100
        self.death_buttons.append(menu_button)

    def remove_death_buttons(self):
        # Удаляем "кнопки смерти"
        for button in self.death_buttons:
            self.ui_manager.remove(button)
        self.death_buttons.clear()

    def restart_game(self, event=None):
        # Начинаем игру сначала
        self.all_sprite.clear()
        self.enemies_sprites.clear()

        self.score = 0

        self.remove_death_buttons()

        # Восстанавливаем игрока
        self.player = Player_Potap()
        self.all_sprite.append(self.player)

        self.level = 1
        self.tile_map = arcade.load_tilemap(f"../static/levels/level{self.level}.tmx", scaling=TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Обновляем физический движок с новым игроком
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.scene["earth"],
            gravity_constant=GRAVITY
        )

        # Сбрасываем камеру
        self.world_camera.position = (self.player.center_x, self.player.center_y)

        # Сбрасываем управление
        self.left_pressed = False
        self.right_pressed = False

        # Включаем музыку
        if self.music_enabled:
            self.music_player = arcade.play_sound(self.music, loop=True, volume=VOLUME)


        for i in self.scene["enemies"]:
            enemy = Enemy(self.scene["earth"])
            enemy.position = i.position
            self.enemies_sprites.append(enemy)
            self.all_sprite.append(enemy)

    def return_to_menu(self, event=None):
        # Возвращаемся в главное меню
        from main import FishHunterMenu
        self.window.show_view(FishHunterMenu())

    def collision_with_enemies(self, player, enemies, type):
        # Проверка коллизии с препятствиями (кроме пропастей)
        collision_list = arcade.check_for_collision_with_list(player, enemies)
        if collision_list and player.alive:
            # Убиваем персонажа
            if type == "spike":
                player.die()
            elif type == "enemy":
                for enemy in collision_list:
                    if player.bottom + 10 <= enemy.top and not self.cheating:
                    # + 10 из-за того что проверка коллизии происходит каждые 1/60 секуды, а не 0
                        player.die()
                    else:
                        enemy.die()
                        self.score += 1000

    def collision_with_items(self, player, item_name):
        # Проверка коллизии с предметами
        collision_list = arcade.check_for_collision_with_list(player, self.scene[item_name])
        if collision_list:
            if item_name == "fish1":
                self.score += 100
            if item_name == "fish3":
                self.score += 200
            if item_name == "fish4":
                self.score += 500
        for item in collision_list:
            item.remove_from_sprite_lists()

    def collision_with_exit(self, player):
        # Проверка коллизии с выходом (нужно перейти на следующий уровень)
        # У слоя exit нулевая непрозрачность
        collision_list = arcade.check_for_collision_with_list(player, self.scene["exit"])
        if collision_list:
            self.moving_to_next_level()

    def moving_to_next_level(self):
        self.all_sprite.clear()
        self.enemies_sprites.clear()
        self.level += 1
        self.tile_map = arcade.load_tilemap(f"../static/levels/level{self.level}.tmx", scaling=TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        for i in self.scene["enemies"]:
            enemy = Enemy(self.scene["earth"])
            enemy.position = i.position
            self.enemies_sprites.append(enemy)
            self.all_sprite.append(enemy)
        self.player.die()
        self.player = Player_Potap()
        self.all_sprite.append(self.player)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.scene["earth"],
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.scene.draw()
        self.all_sprite.draw()
        self.gui_camera.use()
        self.ui_manager.draw()

        # Рисуем счет (сверху)
        arcade.draw_text(
            f"Счет: {self.score}",
            SCREEN_WIDTH - 20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20,
            anchor_x="right",
            anchor_y="top",
            bold=True
        )

        # Если персонаж мертв - рисуем экран смерти
        if not self.player.alive:
            # Сообщение о смерти
            arcade.draw_text(
                "ВЫ УМЕРЛИ",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 80,
                arcade.color.RED,
                48,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

            # Финальный счет
            arcade.draw_text(
                f"Финальный счет: {self.score}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 20,
                arcade.color.WHITE,
                30,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

            # Создаем кнопки, если их еще нет
            if not self.death_buttons:
                self.create_death_buttons()

    def on_update(self, delta_time):
        # Обновляем только если персонаж жив
        if self.player.alive:
            if not self.cheating:
                self.collision_with_enemies(self.player, self.scene["spikes"], "spike")
            self.collision_with_enemies(self.player, self.enemies_sprites, "enemy")
            for i in range(1, 9):
                self.collision_with_items(self.player, f"fish{i}")
            self.collision_with_exit(self.player)

            for i in self.enemies_sprites:
                i.update_movement()
                i.update_animation(delta_time)

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

            cam_x = max(half_w, min(WORLD_PARAMETRS[f"level{self.level}"][0] - half_w, smooth[0]))
            cam_y = max(half_h, min(WORLD_PARAMETRS[f"level{self.level}"][1] - half_h, smooth[1]))
            self.world_camera.position = (cam_x, cam_y)
        else:
            arcade.stop_sound(self.music_player)

        # Обновляем UI
        self.ui_manager.on_update(delta_time)

        self.gui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def on_key_press(self, key, modifiers):
        # Блокируем управление если персонаж мертв
        if not self.player.alive:
            return

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.SPACE and self.physics_engine.can_jump(y_distance=1):
            self.player.jump()
            self.physics_engine.jump(15)

        if key == arcade.key.P:
            if self.music_enabled:
                self.music_enabled = False
                arcade.stop_sound(self.music_player)
            else:
                self.music_enabled = True
                self.music_player = arcade.play_sound(self.music, loop=True, volume=VOLUME)

        # Для отладки (дебага)
        if key == arcade.key.T:
            if not self.cheating:
                self.cheating = True
            else:
                self.cheating = False

    def on_key_release(self, key, modifiers):
        # Блокируем управление если персонаж мертв
        if not self.player.alive:
            return

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_hide_view(self):
        # Деактивируем менеджер UI
        self.ui_manager.disable()

    def on_show_view(self):
        # Активируем менеджер UI
        self.ui_manager.enable()
