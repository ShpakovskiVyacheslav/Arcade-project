# РАЗМЕРЫ ЭКРАНА
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Fish_hunter"

# ФИЗИКА
GRAVITY = 0.5
TILE_SCALING = 1
PLATFORM_TOP = 60

# КАМЕРА
CAMERA_LERP = 0.12

# ПАРАМЕТРЫ МИРОВ (ширина, высота)
WORLD_PARAMETRS = {
    "level1": (3150, 1200),
    "level2": (4200, 1200),
    "level3": (4200, 2500)
}

# ЗВУК
VOLUME = 0.1

# БАФФЫ И ПРЕДМЕТЫ
BIG_JUMP_DELTA_CONST = 2
SMALL_JUMP_HEIGHT = 12
SPEED_DELTA_CONST = 1

# РЕЖИМ ЯРОСТИ
RAGE_SCALE = 0.4
RAGE_BUFF_DURATION = 5

# ЦВЕТА ДЛЯ ЧАСТИЦ ФЕЙЕРВЕРКА
PARTICLE_COLORS = [
    (255, 0, 0), (255, 69, 0), (255, 140, 0),
    (255, 215, 0), (255, 255, 0), (255, 20, 147),
    (255, 0, 255), (218, 112, 214), (138, 43, 226),
    (75, 0, 130), (0, 255, 0), (50, 205, 50),
    (0, 255, 127), (0, 250, 154), (255, 105, 180),
    (220, 20, 60), (178, 34, 34), (128, 0, 0),
    (255, 99, 71), (255, 127, 80), (255, 165, 0),
    (255, 228, 181), (255, 250, 205), (255, 255, 224)
]

# ИЗМЕНЯЕМЫЕ ФАЙЛЫ
MODIFY_FILES = {"db": ["for_database/records.sqlite", "records.sqlite"],
                "settings": ["settings/settings.json", "settings.json"]}
