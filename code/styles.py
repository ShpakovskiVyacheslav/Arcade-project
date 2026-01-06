import arcade
# Стиль для кнопок в главном меню
STYLE = {
            "normal": {
                "font_name": ("calibri", "arial"),
                "font_size": 15,
                "font_color": arcade.color.BLACK_OLIVE,
                "bg": arcade.color.LIGHT_BLUE,
                "border": arcade.color.BLACK_OLIVE,
                "border_width": 2
            },
            "hover": {"font_name": ("calibri", "arial"),
                      "font_size": 15,
                      "font_color": arcade.color.LIGHT_BLUE,
                      "bg": arcade.color.BLACK_OLIVE,
                      "border": arcade.color.BLACK_OLIVE,
                      "border_width": 2},
            "press": {"font_name": ("calibri", "arial"),
                      "font_size": 15,
                      "font_color": arcade.color.LIGHT_BLUE,
                      "bg": arcade.color.BLACK_OLIVE,
                      "border": arcade.color.BLACK_OLIVE,
                      "border_width": 2}
        }

# Стиль для кнопок победы
VICTORY_BUTTON_STYLE = {
            "normal": {
                "font_name": ("calibri", "arial"),
                "font_size": 15,
                "font_color": arcade.color.WHITE,
                "bg": arcade.color.DARK_BLUE,
                "border": arcade.color.BLUE,
                "border_width": 2
            },
            "hover": {
                "font_name": ("calibri", "arial"),
                "font_size": 15,
                "font_color": arcade.color.DARK_BLUE,
                "bg": arcade.color.WHITE,
                "border": arcade.color.BLUE,
                "border_width": 2
            },
            "press": {
                "font_name": ("calibri", "arial"),
                "font_size": 15,
                "font_color": arcade.color.DARK_BLUE,
                "bg": arcade.color.LIGHT_BLUE,
                "border": arcade.color.BLUE,
                "border_width": 2
            }
        }

# Стиль для кнопок смерти
DEATH_BUTTON_STYLE = {
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
