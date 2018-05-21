import math
import pygame
import pygame.gfxdraw
import ui.common
import ui.fonts as fonts
from ui.colors import Color
from ui.component import Component
from states import State

class OverrideLabel(Component):
    def __init__(self):
        super().__init__(169, 28, 141, 40)

    def on_repaint(self, screen):
        font = fonts.get_font(fonts.FontType.ROBOTO_MEDIUM.value, 36)
        text = font.render('Why?', True, Color.RIIT_DARKER_GRAY.value, Color.WHITE.value)
        centered_rect = ui.common.center(text, *self.bounds())
        screen.blit(text, centered_rect)

    def on_press(self, x, y):
        pass

    def on_click(self, x, y):
        pass

class OverrideReasonOption(Component):
    def __init__(self, device, label, number):
        super().__init__(33, 92 + (76 * (number - 1)), 414, 47)
        self.device = device
        self.label = label
        self.number = number
        self.color = Color.RIIT_LIGHT_GRAY.value

    def on_repaint(self, screen):
        pygame.draw.rect(screen, self.color, self.bounds())
        font = fonts.get_font(fonts.FontType.ROBOTO_MEDIUM.value, 24)
        text = font.render(self.label, True, Color.BLACK.value, self.color)
        centered_rect = ui.common.center(text, *self.bounds())
        screen.blit(text, centered_rect)

    def on_press(self, x, y):
        self.color = Color.RIIT_GRAY.value
        self.repaint()

    def on_click(self, x, y):
        self.color = Color.RIIT_LIGHT_GRAY.value
        self.repaint()
        print('chose override option {}: {}'.format(self.number, self.label))
        self.device.set_state(State.DISPENSING)
        self.device.selected_prescription.use(self.device.desired_dose)
        self.device.dispense(self.device.desired_dose)
