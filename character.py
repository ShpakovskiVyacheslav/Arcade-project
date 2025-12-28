import arcade
import enum


# Делаем класс для направления взгляда персонажа,
class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Fish_hunter"
PLATFORM_TOP = 60


class Potap(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Основные характеристики
        self.scale = 1  # если поставьте больше 1 работать будет криво
        self.speed = 5

        # Физические параметры
        self.dx = 0
        self.dy = 0
        self.gravity = 0.5
        self.jump_speed = 15

        # Загрузка текстур
        self.idle_texture = arcade.load_texture("static/images/cat/Cat_stand.png")
        self.texture = self.idle_texture

        self.walk_textures = []
        for i in range(3):
            texture = arcade.load_texture(f"static/images/cat/Cat_sprint_{i}.png")
            self.walk_textures.append(texture)

        self.jump_textures = []
        for i in range(5):
            texture = arcade.load_texture(f"static/images/cat/Cat_jump_{i}.png")
            self.jump_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1  # секунд на кадр

        self.is_walking = False
        self.is_jumping = False
        self.face_direction = FaceDirection.RIGHT

        # Начальная позиция
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = PLATFORM_TOP + 100  # Над платформой

    def update_animation(self, delta_time: float = 1 / 60):
        # Обновление анимации
        if self.is_jumping:
            # Анимация прыжка в зависимости от скорости по Y
            if self.dy > 10:
                texture_index = 0
            elif self.dy > 5:
                texture_index = 1
            elif self.dy > 1:
                texture_index = 2
            elif self.dy < -1:
                texture_index = 3
            else:
                texture_index = 4

            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.jump_textures[texture_index]
            else:
                self.texture = self.jump_textures[texture_index].flip_horizontally()

        elif self.is_walking:
            # Анимация ходьбы
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0

                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()
        else:
            # Анимация покоя
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()

    def update_movement(self):
        # Физика персонажа
        # Гравитация
        self.dy -= self.gravity

        # Перемещение
        self.center_x += self.dx
        self.center_y += self.dy

        # Ограничение движения по горизонтали
        if self.center_x < self.width / 2:
            self.center_x = self.width / 2
        if self.center_x > SCREEN_WIDTH - self.width / 2:
            self.center_x = SCREEN_WIDTH - self.width / 2

        # Проверка столкновения с платформой
        platform_top = PLATFORM_TOP
        if self.center_y - self.height / 2 < platform_top:
            self.center_y = platform_top + self.height / 2
            self.dy = 0
            self.is_jumping = False

        # Определение состояния для анимации
        self.is_walking = abs(self.dx) > 0.1
        self.is_jumping = self.dy != 0 or abs(self.dy) > 0.1

    def move_left(self):
        self.dx = -self.speed
        self.face_direction = FaceDirection.LEFT

    def move_right(self):
        self.dx = self.speed
        self.face_direction = FaceDirection.RIGHT

    def stop_horizontal(self):
        self.dx = 0

    def jump(self):
        # Прыжок возможен только если персонаж стоит на платформе
        if self.center_y - self.height / 2 <= PLATFORM_TOP + 1:
            self.dy = self.jump_speed
            self.is_jumping = True
