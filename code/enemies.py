import arcade


class Enemy(arcade.Sprite):
    def __init__(self, platform_list):
        super().__init__()

        self.platform_list = platform_list
        self.scale = 1
        self.speed = 4

        self.walk_textures = []
        for i in range(8):
            texture = arcade.load_texture(f"../static/images/enemy/dog_{i}.png")
            self.walk_textures.append(texture)

        self.x_frame_animation = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1

        self.face_direction = 1

    def update_animation(self, delta_time: float = 1 / 60):
        self.texture_change_time += delta_time
        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time = 0
            self.x_frame_animation += 1
            if self.x_frame_animation >= len(self.walk_textures):
                self.x_frame_animation = 0

            if self.face_direction == 1:
                self.texture = self.walk_textures[self.x_frame_animation]
            else:
                self.texture = self.walk_textures[self.x_frame_animation].flip_horizontally()

    def update_movement(self):
        # Проверка есть ли земля впереди
        check_x = self.center_x + (self.width / 2 + 10) * self.face_direction
        check_y = self.center_y - self.height / 2 - 20

        sensor = arcade.SpriteSolidColor(10, 10, center_x=check_x, center_y=check_y, color=(255, 0, 0, 0))

        # Если впереди нет платформы - разворачиваемся
        collisions = arcade.check_for_collision_with_list(sensor, self.platform_list)
        if not collisions:
            self.face_direction *= -1

        # Также проверяем столкновение со стеной
        wall_collisions = arcade.check_for_collision_with_list(self, self.platform_list)
        if wall_collisions:
            self.face_direction *= -1

        # Перемещение
        self.center_x += self.speed * self.face_direction

    def die(self):
        self.remove_from_sprite_lists()
