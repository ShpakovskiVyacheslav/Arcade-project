import arcade
from functions import resource_path


class PlayerPotap(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # ФЛАГИ СОСТОЯНИЯ
        self.alive = True
        self.is_walking = False
        self.is_jumping = False
        self.face_direction = True

        # ОСНОВНЫЕ ПАРАМЕТРЫ
        self.scale = 1.2
        self.speed = 5
        self.jump_speed = 15

        # ФИЗИЧЕСКИЕ ПАРАМЕТРЫ
        self.dx = 0
        self.dy = 0

        # ПАРАМЕТРЫ АНИМАЦИИ
        self.x_frame_animation = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр

        self.jump_time = 0
        self.jump_time_animation = 0.5
        self.y_frame_animation = 0

        # НАЧАЛЬНАЯ ПОЗИЦИЯ
        self.center_x = 100
        self.center_y = 400  # Над платформой

        # ЗАГРУЗКА ТЕКСТУР
        self.load_textures()

    def load_textures(self):
        """Загружает все текстуры персонажа."""
        # Текстура покоя
        self.idle_texture = arcade.load_texture(resource_path("static/images/cat/Cat_stand.png"))
        self.texture = self.idle_texture

        # Текстуры ходьбы (3 кадра)
        self.walk_textures = []
        for frame_num in range(3):
            texture_path = resource_path(f"static/images/cat/Cat_sprint_{frame_num}.png")
            texture = arcade.load_texture(texture_path)
            self.walk_textures.append(texture)

        # Текстуры прыжка (6 кадров)
        self.jump_textures = []
        for frame_num in range(6):
            texture_path = resource_path(f"static/images/cat/Cat_jump_{frame_num}.png")
            texture = arcade.load_texture(texture_path)
            self.jump_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):
        """Обновление анимации персонажа."""

        # Анимация прыжка
        if self.is_jumping:
            self.update_jump_animation()

        # Анимация ходьбы
        elif self.is_walking:
            self.update_walk_animation(delta_time)

        # Анимация покоя
        else:
            self.update_idle_animation()

    def update_jump_animation(self):
        """Обновление анимации прыжка."""
        # Определяем индекс текстуры в зависимости от скорости по Y
        if self.change_y > 10:
            texture_index = 0
        elif self.change_y > 3:
            texture_index = 2
        elif 3 >= self.change_y >= -3:
            texture_index = 3
        elif self.change_y < -15:
            texture_index = 5
        elif self.change_y < -3:
            texture_index = 4
        else:
            texture_index = 4

        # Применяем текстуру с учетом направления
        if self.face_direction:
            self.texture = self.jump_textures[texture_index]
        else:
            self.texture = self.jump_textures[texture_index].flip_horizontally()

    def update_walk_animation(self, delta_time):
        """Обновление анимации ходьбы."""
        self.texture_change_time += delta_time

        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time = 0
            self.x_frame_animation += 1

            if self.x_frame_animation >= len(self.walk_textures):
                self.x_frame_animation = 0

            # Применяем текстуру с учетом направления
            if self.face_direction:
                self.texture = self.walk_textures[self.x_frame_animation]
            else:
                flipped_texture = self.walk_textures[self.x_frame_animation].flip_horizontally()
                self.texture = flipped_texture

    def update_idle_animation(self):
        """Обновление анимации покоя."""
        if self.face_direction:
            self.texture = self.idle_texture
        else:
            self.texture = self.idle_texture.flip_horizontally()

    def update_movement(self):
        """Обновление движения и проверка состояния."""
        # Проверка падения за экран
        if self.center_y < 0:
            self.die()

        # Перемещение по горизонтали с проверкой границ
        if not (self.left <= 0 and self.dx < 0):
            self.center_x += self.dx

        # Перемещение по вертикали
        self.center_y += self.dy

        # Определение состояния для анимации
        self.is_walking = abs(self.dx) > 0.1
        self.is_jumping = self.change_y != 0

    def move_left(self):
        """Движение влево."""
        self.dx = -self.speed
        self.face_direction = False

    def move_right(self):
        """Движение вправо."""
        self.dx = self.speed
        self.face_direction = True

    def stop_horizontal(self):
        """Остановка горизонтального движения."""
        self.dx = 0

    def jump(self):
        """Фцнкуция прыжка"""
        self.is_jumping = True

    def die(self):
        """Обработка смерти персонажа."""
        self.alive = False
        self.remove_from_sprite_lists()

    def respawn(self, x=100, y=400):
        """Возрождение персонажа в указанных координатах."""
        self.alive = True
        self.center_x = x
        self.center_y = y

        # Сброс движения
        self.dx = 0
        self.dy = 0
        self.change_x = 0
        self.change_y = 0

        # Сброс состояний
        self.is_jumping = False
        self.is_walking = False
