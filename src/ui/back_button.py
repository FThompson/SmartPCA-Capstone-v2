import pygame
import pygame.gfxdraw
from ui.colors import Color
from ui.component import Component

BACK_ARROW_POINTS = ((28, 8), (8, 28), (28, 48), (30, 46), (10, 28), (30, 10))

class BackButton(Component):
    def __init__(self, device, state):
        super().__init__(8, 8, 40, 40)
        self.device = device
        self.state = state
        self.color = Color.RIIT_DARKER_GRAY.value

    def on_repaint(self, screen):
        pygame.gfxdraw.aapolygon(screen, BACK_ARROW_POINTS, self.color)
        pygame.gfxdraw.filled_polygon(screen, BACK_ARROW_POINTS, self.color)

    def on_press(self, x, y):
        self.color = Color.BLACK.value
        self.repaint()

    def on_click(self, x, y):
        self.color = Color.RIIT_DARKER_GRAY.value
        self.repaint()
        self.device.set_state(self.state)
