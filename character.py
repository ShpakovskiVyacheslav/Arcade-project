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
        self.scale = 3.0
        self.speed = 300

        # Загрузка текстур
        self.idle_texture = arcade.load_texture(
            "static/images/cat/Cat_stand.png",)
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

        self.is_walking_x = False
        self.is_walking_y = False
        self.face_direction = FaceDirection.RIGHT

        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

        self.dx, self.dy = 0, 0

    def update_animation(self, delta_time: float = 1 / 60):
        # Обновление анимации
        if self.is_walking_y:
            if self.dy > 10:
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.jump_textures[0]
                else:
                    self.texture = self.jump_textures[0].flip_horizontally()
            elif self.dy > 5:
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.jump_textures[1]
                else:
                    self.texture = self.jump_textures[1].flip_horizontally()
            if self.dy > 1:
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.jump_textures[2]
                else:
                    self.texture = self.jump_textures[2].flip_horizontally()
            elif self.dy < 10:
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.jump_textures[4]
                else:
                    self.texture = self.jump_textures[4].flip_horizontally()
            elif self.dy < 1:
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.jump_textures[3]
                else:
                    self.texture = self.jump_textures[3].flip_horizontally()
            else:
                # Если не идём, то просто показываем текстуру покоя
                # и поворачиваем её в зависимости от направления взгляда
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.idle_texture
                else:
                    self.texture = self.idle_texture.flip_horizontally()

        elif self.is_walking_x:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                # Поворачиваем текстуру в зависимости от направления взгляда
                if self.face_direction == FaceDirection.RIGHT:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()

        else:
            # Если не идём, то просто показываем текстуру покоя
            # и поворачиваем её в зависимости от направления взгляда
            if self.face_direction == FaceDirection.RIGHT:
                self.texture = self.idle_texture
            else:
                self.texture = self.idle_texture.flip_horizontally()


    def update(self, delta_time, keys_pressed):
        # Перемещение персонажа
        # В зависимости от нажатых клавиш определяем направление движения

        self.dy -= 0.5
        if arcade.key.LEFT in keys_pressed or arcade.key.A in keys_pressed:
            self.dx -= self.speed * delta_time
        if arcade.key.RIGHT in keys_pressed or arcade.key.D in keys_pressed:
            self.dx += self.speed * delta_time
        elif arcade.key.SPACE in keys_pressed:
            # Прыгаем только если стоим на платформе
            if self.dy == 0:
                self.dy = 15  # скорость прыжка

        if self.dx != 0 and self.dy != 0:
            factor = 0.7071
            self.dx *= factor
            self.dy *= factor
        self.center_x += self.dx
        self.center_y += self.dy
        # Поворачиваем персонажа в зависимости от направления движения
        if self.dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif self.dx > 0:
            self.face_direction = FaceDirection.RIGHT

        # Ограничение в пределах экрана
        self.center_x = max(self.width / 2, min(SCREEN_WIDTH - self.width / 2, self.center_x))
        self.center_y = max(self.height / 2, min(SCREEN_HEIGHT - self.height / 2, self.center_y))

        # Проверка на движение
        self.is_walking_x = self.dx
        self.is_walking_y = self.dy
