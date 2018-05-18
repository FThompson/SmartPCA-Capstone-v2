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

# takes text surface returned by Font.render
# returns rectangle to be passed to screen.blit with text surface
# pass 0 to width for only-vertical centering, 0 to height for only-horizontal centering
def center(text, x, y, w=0, h=0):
    return text.get_rect(center=(x + w / 2, y + h / 2))
