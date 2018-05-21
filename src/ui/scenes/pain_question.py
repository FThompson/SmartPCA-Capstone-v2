from enum import Enum

import pygame
import ui.common
import util.images
from states import State
from ui.button import QuestionButton
from ui.colors import Color
from ui.component import Component
from util.time import millis

class PainQuestion(Enum):
    DAILY = ('How is your pain being', 'managed overall?'), 24 * 60 * 60 * 1000
    REGULAR = ('How bad is your', 'pain right now?'), 10 * 60 * 1000

    def __init__(self, lines, ask_window):
        self.lines = lines
        self.ask_window = ask_window
        self.last_ask_time = 0

    def should_ask(self):
        return self.last_ask_time == 0 or millis() - self.last_ask_time > self.ask_window

    def update_ask_time(self):
        self.last_ask_time = millis()

    @classmethod
    def get_current_question(cls):
        for question in cls:
            if question.should_ask():
                return question
        return None

class PainQuestionLabel(Component):
    def __init__(self, device):
        super().__init__(0, 0, 480, 191)
        self.device = device

    def on_repaint(self, screen):
        pygame.draw.rect(screen, Color.WHITE.value, (0, 53, 480, 89))
        ui.common.render_question(screen, self.device.pain_question.lines)

    def on_press(self, x, y):
        pass

    def on_click(self, x, y):
        pass

class FaceOption(QuestionButton):
    def __init__(self, device, face, x):
        self.device = device
        self.face = face
        super().__init__(x, 191, 118, 129, Color.RIIT_LIGHT_GRAY.value)

    def get_surface(self):
        return util.images.load_image('face{}.png'.format(self.face))

    def on_press(self, x, y):
        self.color = Color.RIIT_GRAY.value
        self.repaint()

    def on_click(self, x, y):
        self.color = Color.RIIT_LIGHT_GRAY.value
        self.repaint()
        self.device.pain_question.update_ask_time()
        print('answered {} q with face {}'.format(str(self.device.pain_question), self.face))
        if self.device.has_pain_question():
            self.device.scene.repaint()
        else:
            self.device.set_state(State.REQUEST_DOSE)
