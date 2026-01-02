import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Fish_hunter"
CAMERA_LERP = 0.12
GRAVITY = 0.5


class Player_Potap(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.alive = True  # флаг жизни

        # Основные характеристики
        self.scale = 1
        self.speed = 5

        # Физические параметры
        self.dx = 0
        self.dy = 0
        self.jump_speed = 15

        # Загрузка текстур
        self.idle_texture = arcade.load_texture("static/images/cat/Cat_stand.png")
        self.texture = self.idle_texture

        self.walk_textures = []
        for i in range(3):
            texture = arcade.load_texture(f"static/images/cat/Cat_sprint_{i}.png")
            self.walk_textures.append(texture)

        self.jump_textures = []
        for i in range(6):
            texture = arcade.load_texture(f"static/images/cat/Cat_jump_{i}.png")
            self.jump_textures.append(texture)

        self.x_frame_animation = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр
        self.jump_time = 0
        self.jump_time_animation = 0.5
        self.y_frame_animation = 0

        self.is_walking = False
        self.is_jumping = False
        self.face_direction = True

        # Начальная позиция
        self.center_x = 100
        self.center_y = 400  # Над платформой

    def update_animation(self, delta_time: float = 1 / 60):
        # Обновление анимации
        if self.is_jumping:
            # Анимация прыжка в зависимости от скорости по Y
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

            if self.face_direction:
                self.texture = self.jump_textures[texture_index]
            else:
                self.texture = self.jump_textures[texture_index].flip_horizontally()


        elif self.is_walking:
            # Анимация ходьбы
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.x_frame_animation += 1
                if self.x_frame_animation >= len(self.walk_textures):
                    self.x_frame_animation = 0

                if self.face_direction:
                    self.texture = self.walk_textures[self.x_frame_animation]
                else:
                    self.texture = self.walk_textures[self.x_frame_animation].flip_horizontally()
        else:
            # Анимация покоя
            if self.face_direction:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()

    def update_movement(self):
        if self.center_y < 0:
            self.die()
        # Перемещение
        self.center_x += self.dx
        self.center_y += self.dy

        # Определение состояния для анимации
        self.is_walking = abs(self.dx) > 0.1
        self.is_jumping = self.change_y != 0

    def move_left(self):
        self.dx = -self.speed
        self.face_direction = False

    def move_right(self):
        self.dx = self.speed
        self.face_direction = True

    def stop_horizontal(self):
        self.dx = 0

    def jump(self):
        # Прыжок возможен только если персонаж стоит на платформе
        # self.dy = self.jump_speed
        self.is_jumping = True

    def die(self):
        self.alive = False
        self.remove_from_sprite_lists()

    def respawn(self, x=100, y=400):
        # Возродить персонажа
        self.alive = True
        self.center_x = x
        self.center_y = y
        self.dx = 0
        self.dy = 0
        self.change_x = 0
        self.change_y = 0
        self.is_jumping = False
        self.is_walking = False
