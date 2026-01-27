import sqlite3
import random
from arcade.gui import UIFlatButton, UIManager
from character import PlayerPotap
from arcade.camera import Camera2D
from constants import *
from styles import *
from enemies import Enemy
from arcade.particles import FadeParticle, Emitter, EmitBurst
from functions import resource_path, get_database_path


class FishHunterGame(arcade.View):
    def __init__(self, CONTROLS):
        super().__init__()
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.world_camera = Camera2D()
        self.gui_camera = Camera2D()

        # UI менеджер для кнопок
        self.ui_manager = UIManager()
        self.ui_manager.enable()

        # Создаем игрока
        self.all_sprite = arcade.SpriteList()
        self.player = PlayerPotap()
        self.all_sprite.append(self.player)

        # Создаем список врагов
        self.enemies_sprites = arcade.SpriteList()

        # Управление
        self.left_pressed = False
        self.right_pressed = False

        self.level = 1
        self.tile_map = arcade.load_tilemap(resource_path(f"static/levels/level{self.level}.tmx"), scaling=TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.CONTROLS = CONTROLS

        # Создаем врагов
        for i in self.scene["enemies"]:
            enemy = Enemy(self.scene["earth"])
            enemy.position = i.position
            self.enemies_sprites.append(enemy)
            self.all_sprite.append(enemy)
        self.score = 0

        # Кнопки (будут показаны при смерти/победе)
        self.buttons = []
        self.victory_mode = False

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.scene["earth"],
            gravity_constant=GRAVITY
        )

        self.music = arcade.load_sound(resource_path("static/sounds/background music.mp3"))
        self.music_player = arcade.play_sound(self.music, loop=True, volume=VOLUME)
        self.music_enabled = True

        self.cheating = False
        self.rage = False
        self.check_saving = True

        self.jump_height = 15

        self.active_buffs = []

        self.fireworks = []
        self.firework_textures = []

        # Создаем текстуры для фейерверков
        for color in PARTICLE_COLORS:
            self.firework_textures.append(arcade.make_soft_circle_texture(15, color, 255))

        self.items = {
            # Рыбы, дающие очки
            "fish1": lambda: setattr(self, 'score', self.score + 100),
            "fish3": lambda: setattr(self, 'score', self.score + 200),
            "fish4": lambda: setattr(self, 'score', self.score + 500),

            # Рыбы, дающие бафф
            "fish2": lambda: setattr(self, 'jump_height', self.jump_height + BIG_JUMP_DELTA_CONST),
            "fish5": lambda: setattr(self.player, 'speed', self.player.speed + SPEED_DELTA_CONST),

            # Особый обработчик для fish6 с дополнительной логикой
            "fish6": lambda: self.apply_active_buff(self.player),

            # Фейерверк
            "fireworks": lambda: self.create_firework(self.player.center_x, self.player.center_y + 200)
        }

    def create_buttons(self, victory=False):
        # Создаем кнопки для экрана смерти или победы
        # Очищаем старые кнопки
        for button in self.buttons:
            self.ui_manager.remove(button)
        self.buttons.clear()

        # Выбираем стиль в зависимости от режима
        style = VICTORY_BUTTON_STYLE if victory else DEATH_BUTTON_STYLE

        button_parameters = [("Начать заново", self.restart_game), ("Сохранить результат", self.save_result_window),
                             ("Вернуться в меню", self.return_to_menu)]

        for i in range(3):
            button = UIFlatButton(
                text=button_parameters[i][0],
                width=200,
                height=40,
                style=style
            )
            button.on_click = button_parameters[i][1]
            self.ui_manager.add(button)
            button.center_x = SCREEN_WIDTH // 2
            button.center_y = SCREEN_HEIGHT // 2 - i * 50 - 50
            self.buttons.append(button)

    def remove_buttons(self):
        for button in self.buttons:
            self.ui_manager.remove(button)
        self.buttons.clear()

    def restart_game(self, event=None):
        # Начинаем игру сначала
        self.all_sprite.clear()
        self.enemies_sprites.clear()

        self.score = 0

        self.remove_buttons()

        # Восстанавливаем игрока
        self.player = PlayerPotap()
        self.all_sprite.append(self.player)

        self.level = 1
        self.tile_map = arcade.load_tilemap(resource_path(f"static/levels/level{self.level}.tmx"), scaling=TILE_SCALING)
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

        # Создаем врагов
        for i in self.scene["enemies"]:
            enemy = Enemy(self.scene["earth"])
            enemy.position = i.position
            self.enemies_sprites.append(enemy)
            self.all_sprite.append(enemy)
        self.fireworks.clear()

        self.jump_height = 15
        self.rage = False
        self.cheating = False
        self.check_saving = True
        self.active_buffs.clear()
        self.victory_mode = False

    def return_to_menu(self, event=None):
        # Возвращаемся в главное меню
        from main import FishHunterMenu
        self.window.show_view(FishHunterMenu())

    def save_result_window(self, event=None):
        if self.check_saving:
            conn = sqlite3.connect(get_database_path())
            cursor = conn.cursor()

            # НЕ указываем id - он сгенерируется автоматически
            cursor.execute(f'''
                INSERT INTO results (result)
                VALUES ({self.score})
            ''')
            conn.commit()
            conn.close()
            self.check_saving = False

    def collision_with_enemies(self, player, enemies, type):
        # Проверка коллизии с препятствиями (кроме пропастей)
        collision_list = arcade.check_for_collision_with_list(player, enemies)
        if collision_list and player.alive:
            # Убиваем персонажа
            if type == "spike":
                player.die()
            elif type == "enemy":
                for enemy in collision_list:
                    if player.bottom + 25 <= enemy.top and not (self.cheating or self.rage):
                        # + 25 из-за того что проверка коллизии происходит каждые 1/60 секуды, а не 0
                        player.die()
                    else:
                        enemy.die()
                        self.score += 1000

    def collision_with_items(self, player, item_name):
        # Проверка коллизии с предметами
        collision_list = arcade.check_for_collision_with_list(player, self.scene[item_name])

        if collision_list:
            item = self.items.get(item_name)
            if item:
                item()

            # Удаляем все столкнувшиеся предметы
            for item in collision_list:
                item.remove_from_sprite_lists()

            for item in collision_list:
                item.remove_from_sprite_lists()

    def apply_active_buff(self, player):
        # Вспомогательная функция для обработки актиыных баффов
        player.scale = 1.4
        self.rage = True

        # Ищем существующий бафф RAGE
        for buff in self.active_buffs:
            if buff[0] == "RAGE":
                buff[1] += RAGE_BUFF_DURATION
                break
        else:
            # Если бафф не найден, добавляем новый
            self.active_buffs.append(["RAGE", RAGE_BUFF_DURATION])

    def collision_with_exit(self, player):
        # Проверка коллизии с выходом (нужно перейти на следующий уровень)

        collision_list = arcade.check_for_collision_with_list(player, self.scene["exit"])
        if collision_list:
            self.moving_to_next_level()

    def moving_to_next_level(self):
        next_level = self.level + 1
        try:
            test_map = arcade.load_tilemap(f"../static/levels/level{next_level}.tmx", scaling=TILE_SCALING)
            self.all_sprite.clear()
            self.enemies_sprites.clear()
            self.level = next_level
            self.tile_map = test_map
            self.scene = arcade.Scene.from_tilemap(self.tile_map)

            # Создаем врагов для нового уровня
            for i in self.scene["enemies"]:
                enemy = Enemy(self.scene["earth"])
                enemy.position = i.position
                self.enemies_sprites.append(enemy)
                self.all_sprite.append(enemy)

            self.player.die()
            self.player = PlayerPotap()
            self.all_sprite.append(self.player)
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                player_sprite=self.player,
                platforms=self.scene["earth"],
                gravity_constant=GRAVITY
            )
            self.fireworks.clear()

        except Exception:
            self.show_victory_screen()

    def show_victory_screen(self):
        self.player.alive = False
        self.victory_mode = True
        arcade.stop_sound(self.music_player)
        self.create_buttons(victory=True)

    def create_firework(self, x, y):
        for i in range(10):
            texture = random.choice(self.firework_textures)
            offset_x = random.uniform(-50, 50)
            offset_y = random.uniform(-20, 20)

            particle_count = random.randint(40, 100)
            radius = random.uniform(2, 4)
            lifetime = random.uniform(1.8, 3.5)

            firework = Emitter(
                center_xy=(x + offset_x, y + offset_y),
                emit_controller=EmitBurst(particle_count),
                particle_factory=lambda e, tex=texture, rad=radius, life=lifetime: FadeParticle(
                    filename_or_texture=tex,
                    change_xy=arcade.math.rand_in_circle((0.0, 0.0), rad),
                    lifetime=life,
                    start_alpha=random.randint(200, 255),
                    end_alpha=0,
                    scale=random.uniform(0.2, 0.8))
            )
            self.fireworks.append(firework)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.scene.draw()
        self.all_sprite.draw()

        # Рисуем компактные фейерверки
        for firework in self.fireworks:
            firework.draw()

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

        # Если персонаж мертв - рисуем экран смерти или победы
        if not self.player.alive:
            if self.victory_mode:
                title = "ВЫ ПОБЕДИЛИ!"
                color = arcade.color.GOLD
            else:
                title = "ВЫ УМЕРЛИ"
                color = arcade.color.RED

            # Сообщение о смерти/победе
            arcade.draw_text(
                title,
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 80,
                color,
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
            if not self.buttons:
                self.create_buttons(victory=self.victory_mode)

    def on_update(self, delta_time):
        # Обновляем только если персонаж жив
        if self.player.alive:
            if not (self.cheating or self.rage):
                self.collision_with_enemies(self.player, self.scene["spikes"], "spike")
            self.collision_with_enemies(self.player, self.enemies_sprites, "enemy")
            for i in range(1, 9):
                self.collision_with_items(self.player, f"fish{i}")
            self.collision_with_items(self.player, "fireworks")
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
            smooth = (cx + (tx - cx) * CAMERA_LERP, cy + (ty - cy) * CAMERA_LERP)

            half_w = self.world_camera.viewport_width / 2
            half_h = self.world_camera.viewport_height / 2

            cam_x = max(half_w, min(WORLD_PARAMETRS[f"level{self.level}"][0] - half_w, smooth[0]))
            cam_y = max(half_h, min(WORLD_PARAMETRS[f"level{self.level}"][1] - half_h, smooth[1]))
            self.world_camera.position = (cam_x, cam_y)
        else:
            arcade.stop_sound(self.music_player)

        # Обновляем фейерверки
        for firework in self.fireworks[:]:
            firework.update(delta_time)
            if firework.can_reap():
                self.fireworks.remove(firework)

        self.ui_manager.on_update(delta_time)

        self.gui_camera.position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        # Обновляем активные баффы
        for i in self.active_buffs:
            if i[1] <= 0:
                self.active_buffs.remove(i)
                if i[0] == "RAGE":
                    self.player.scale = 1
                    self.rage = False
            i[1] -= delta_time

    def on_key_press(self, key, modifiers):
        # Блокируем управление если персонаж мертв
        if not self.player.alive:
            return

        if key == self.CONTROLS["move_left"]:
            self.left_pressed = True
        elif key == self.CONTROLS["move_right"]:
            self.right_pressed = True
        elif key == self.CONTROLS["jump_high"] and (self.physics_engine.can_jump(y_distance=1) or self.cheating):
            self.player.jump()
            self.physics_engine.jump(self.jump_height)
        elif key == self.CONTROLS["jump_low"] and (
                self.physics_engine.can_jump(y_distance=1) or self.cheating):
            self.player.jump()
            self.physics_engine.jump(SMALL_JUMP_HEIGHT)

        # Создаем фейерверк
        if key == self.CONTROLS["firework"]:
            self.create_firework(self.player.center_x, self.player.center_y + 200)

        # Управление музыкой
        if key == self.CONTROLS["music"]:
            if self.music_enabled:
                self.music_enabled = False
                arcade.stop_sound(self.music_player)
            else:
                self.music_enabled = True
                self.music_player = arcade.play_sound(self.music, loop=True, volume=VOLUME)

        # Для отладки (дебага)
        if key == self.CONTROLS["debug"]:
            if not self.cheating:
                self.cheating = True
            else:
                self.cheating = False

    def on_key_release(self, key, modifiers):
        # Блокируем управление если персонаж мертв
        if not self.player.alive:
            return

        if key == self.CONTROLS["move_left"]:
            self.left_pressed = False
        elif key == self.CONTROLS["move_right"]:
            self.right_pressed = False

    def on_hide_view(self):
        # Деактивируем менеджер UI
        self.ui_manager.disable()

    def on_show_view(self):
        # Активируем менеджер UI
        self.ui_manager.enable()
