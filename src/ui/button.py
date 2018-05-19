from abc import abstractmethod
import pygame
import ui.common
from ui.component import Component

class QuestionButton(Component):
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, w, h)
        self.color = color
        self.surface = self.get_surface()
        self.centered_rect = ui.common.center(self.surface, *self.bounds())

    @abstractmethod
    def get_surface(self):
        pass

    def on_repaint(self, screen):
        pygame.draw.rect(screen, self.color, self.bounds())
        screen.blit(self.surface, self.centered_rect)
