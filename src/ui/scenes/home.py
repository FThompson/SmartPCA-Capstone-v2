import pygame
import ui.fonts as fonts
from ui.component import Component

class HelloLabel(Component):
    def __init__(self):
        super().__init__(105, 25, 270, 29)

    def on_repaint(self, screen):
        print("painted hello")
        font = fonts.get_font(fonts.FontType.ROBOTO_LIGHT.value, 24)
        text = font.render("Hello.", True, (0, 0, 0), (255, 255, 255))
        centered_rect = fonts.center(text, self.x, self.y, self.w)
        screen.blit(text, centered_rect)

    def on_press(self, x, y):
        print("pressed hello")

    def on_click(self, x, y):
        print("clicked hello")
