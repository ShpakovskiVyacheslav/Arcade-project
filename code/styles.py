import arcade

# Основной фон для меню (морская тематика)
MENU_BACKGROUND_COLOR = (30, 60, 100)

# Стиль для кнопок в главном меню (обновленный)
STYLE = {
    "normal": {
        "font_name": ("calibri", "arial"),
        "font_size": 18,
        "font_color": arcade.color.WHITE,
        "bg": (52, 152, 219),
        "border": (41, 128, 185),
        "border_width": 3,
        "border_radius": 12,
    },
    "hover": {
        "font_name": ("calibri", "arial"),
        "font_size": 18,
        "font_color": arcade.color.WHITE,
        "bg": (41, 128, 185),
        "border": (31, 97, 141),
        "border_width": 3,
        "border_radius": 12,
    },
    "press": {
        "font_name": ("calibri", "arial"),
        "font_size": 18,
        "font_color": (200, 220, 255),
        "bg": (31, 97, 141),
        "border": (21, 67, 96),
        "border_width": 3,
        "border_radius": 12,
    }
}

# Стиль для кнопок победы (золотой/победный)
VICTORY_BUTTON_STYLE = {
    "normal": {
        "font_name": ("calibri", "arial"),
        "font_size": 16,
        "font_color": (255, 215, 0),
        "bg": (75, 0, 130, 180),
        "border": (255, 215, 0),
        "border_width": 2,
        "border_radius": 10,
    },
    "hover": {
        "font_name": ("calibri", "arial"),
        "font_size": 16,
        "font_color": (255, 255, 200),
        "bg": (138, 43, 226, 200),
        "border": (255, 255, 0),
        "border_width": 2,
        "border_radius": 10,
    },
    "press": {
        "font_name": ("calibri", "arial"),
        "font_size": 16,
        "font_color": (255, 255, 200),
        "bg": (106, 13, 173, 200),
        "border": (255, 200, 0),
        "border_width": 2,
        "border_radius": 10,
    }
}

# Стиль для кнопок смерти (красный/драматичный)
DEATH_BUTTON_STYLE = {
    "normal": {
        "font_name": ("calibri", "arial"),
        "font_size": 16,
        "font_color": (255, 240, 240),
        "bg": (178, 34, 34, 180),
        "border": (255, 69, 0),
        "border_width": 2,
        "border_radius": 10,
    },
    "hover": {
        "font_name": ("calibri", "arial"),
        "font_size": 16,
        "font_color": (255, 255, 255),
        "bg": (220, 20, 60, 200),
        "border": (255, 99, 71),
        "border_width": 2,
        "border_radius": 10,
    },
    "press": {
        "font_name": ("calibri", "arial"),
        "font_size": 16,
        "font_color": (255, 255, 255),
        "bg": (139, 0, 0, 200),
        "border": (255, 69, 0),
        "border_width": 2,
        "border_radius": 10,
    }
}

# Стиль для информационных кнопок (результаты, настройки)
INFO_BUTTON_STYLE = {
    "normal": {
        "font_name": ("calibri", "arial"),
        "font_size": 16,
        "font_color": (50, 50, 50),
        "bg": (200, 230, 255),
        "border": (100, 149, 237),
        "border_width": 2,
        "border_radius": 8,
    },
    "hover": {
        "font_name": ("calibri", "arial"),
        "font_size": 16,
        "font_color": (30, 30, 30),
        "bg": (173, 216, 230),
        "border": (70, 130, 180),
        "border_width": 2,
        "border_radius": 8,
    },
    "press": {
        "font_name": ("calibri", "arial"),
        "font_size": 16,
        "font_color": (255, 255, 255),
        "bg": (100, 149, 237),
        "border": (65, 105, 225),
        "border_width": 2,
        "border_radius": 8,
    }
}
