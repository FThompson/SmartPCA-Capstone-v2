import pygame
import pygame.gfxdraw
from ui.colors import Color
from ui.component import Component
from states import State

class MenuButton(Component):
    def __init__(self, device):
        super().__init__(442, 8, 30, 30)
        self.device = device
        self.color = Color.RIIT_DARKER_GRAY.value

    def on_repaint(self, screen):
        pygame.draw.rect(screen, self.color, (self.dx(2), self.dy(4), 26, 4))
        pygame.draw.rect(screen, self.color, (self.dx(2), self.dy(13), 26, 4))
        pygame.draw.rect(screen, self.color, (self.dx(2), self.dy(22), 26, 4))

    def on_press(self, x, y):
        self.color = Color.BLACK.value
        self.repaint()

    def on_click(self, x, y):
        self.color = Color.RIIT_DARKER_GRAY.value
        self.repaint()
        self.device.set_state(State.MENU)
