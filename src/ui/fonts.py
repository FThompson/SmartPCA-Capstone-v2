from enum import Enum

import pygame

class FontType(Enum):
    ROBOTO_LIGHT = ('roboto_light', '/usr/share/fonts/truetype/roboto/hinted/Roboto-Light.ttf')
    ROBOTO_MEDIUM = ('roboto_medium', '/usr/share/fonts/truetype/roboto/hinted/Roboto-Medium.ttf')

fonts = {}

def get_font(font_type, size):
    name, path = font_type
    key = name + '_' + str(size)
    if key not in fonts:
        fonts[key] = pygame.font.Font(path, size)
    return fonts.get(key)
