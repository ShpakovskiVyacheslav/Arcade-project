import arcade


class Enemy(arcade.Sprite):
    def __init__(self, platform_list):
        super().__init__()

        self.platform_list = platform_list

        # ОСНОВНЫЕ ПАРАМЕТРЫ
        self.scale = 1
        self.speed = 4
        self.face_direction = 1

        # ПАРАМЕТРЫ АНИМАЦИИ
        self.x_frame_animation = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр

        # ЗАГРУЗКА ТЕКСТУР
        self.walk_textures = []
        self._load_textures()

    def _load_textures(self):
        # Загружает текстуры врага
        for frame_num in range(8):
            texture_path = f"../static/images/enemy/dog_{frame_num}.png"
            texture = arcade.load_texture(texture_path)
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):
        # Обновление анимации врага
        self.texture_change_time += delta_time

        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time = 0
            self.x_frame_animation += 1

            if self.x_frame_animation >= len(self.walk_textures):
                self.x_frame_animation = 0

            # Применяем текстуру с учетом направления
            if self.face_direction == 1:
                self.texture = self.walk_textures[self.x_frame_animation]
            else:
                flipped_texture = self.walk_textures[self.x_frame_animation].flip_horizontally()
                self.texture = flipped_texture

    def update_movement(self):
        """Обновление движения врага с проверкой препятствий"""
        # Проверка есть ли земля впереди
        check_x = self.center_x + (self.width / 2 + 10) * self.face_direction
        check_y = self.center_y - self.height / 2 - 20

        # Создаем сенсор для проверки земли
        sensor = arcade.SpriteSolidColor(
            width=10,
            height=10,
            center_x=check_x,
            center_y=check_y,
            color=(255, 0, 0, 0)
        )

        # Если впереди нет платформы - разворачиваемся
        collisions = arcade.check_for_collision_with_list(sensor, self.platform_list)
        if not collisions:
            self.face_direction *= -1

        # Также проверяем столкновение со стеной
        wall_collisions = arcade.check_for_collision_with_list(self, self.platform_list)
        if wall_collisions:
            self.face_direction *= -1

        # Перемещение врага
        self.center_x += self.speed * self.face_direction

    def die(self):
        # Удаление врага из игры
        self.remove_from_sprite_lists()
