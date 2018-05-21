import pygame
import pygame.gfxdraw
from ui.colors import Color
from ui.component import Component
from states import State

BACK_ARROW_POINTS = ((23, 8), (8, 23), (23, 38), (25, 36), (12, 23), (25, 10))
#BACK_ARROW_POINTS = ((28, 8), (8, 28), (28, 48), (30, 46), (12, 28), (30, 10))

class BackButton(Component):
    def __init__(self, device):
        super().__init__(8, 8, 30, 30)
        self.device = device
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
        self.set_state_back()

    def set_state_back(self):
        state = self.device.state
        if state == State.PAIN_QUESTION:
            self.device.set_state(State.HOME)
        elif state == State.REQUEST_DOSE:
            if self.device.pain_question is not None:
                self.device.set_state(State.PAIN_QUESTION)
            else:
                self.device.set_state(State.HOME)
        elif state == State.OVERRIDE_DOSE:
            self.device.set_state(State.REQUEST_DOSE)
        elif state == State.OVERRIDE_REASON:
            self.device.set_state(State.OVERRIDE_DOSE)
        elif state == State.MENU:
            self.device.set_state(State.HOME)
        elif state in (State.PRESCRIPTION, State.SETTINGS, State.CONTACT):
            self.device.set_state(State.MENU)
