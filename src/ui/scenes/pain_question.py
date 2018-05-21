import ui.common
import util.images
from ui.button import QuestionButton
from ui.colors import Color
from ui.component import Component
from util.time import millis
from states import State

class Question():
    def __init__(self, key, lines, ask_window):
        self.key = key
        self.lines = lines
        self.last_ask_time = 0
        self.ask_window = ask_window

    def should_ask(self):
        return self.last_ask_time == 0 or millis() - self.last_ask_time > self.ask_window

    def update_ask_time(self):
        self.last_ask_time = millis()

QUESTIONS = (
    Question('daily', ('How is your pain being', 'managed overall?'), 24 * 60 * 60 * 1000),
    Question('regular', ('How bad is your', 'pain right now?'), 10 * 60 * 1000)
)

class PainQuestion(Component):
    def __init__(self, device):
        super().__init__(0, 0, 480, 191)
        self.device = device
        self.question = None

    def update_question(self):
        def get_current_question():
            for question in QUESTIONS:
                if question.should_ask():
                    return question
            return None
        self.question = get_current_question()

    def on_repaint(self, screen):
        self.clear(screen)
        self.update_question()
        # not ideal to place this logic here
        if self.question is None:
            self.device.set_state(State.REQUEST_DOSE)
        else:
            ui.common.render_question(screen, self.question.lines)

    def on_press(self, x, y):
        pass

    def on_click(self, x, y):
        pass

class FaceOption(QuestionButton):
    def __init__(self, device, pain_question, face, x):
        self.device = device
        self.question_label = pain_question
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
        self.question_label.question.update_ask_time()
        print('answered {} q with face {}'.format(self.question_label.question.key, self.face))
        self.question_label.update_question()
        if self.question_label.question is None:
            self.device.set_state(State.REQUEST_DOSE)
        else:
            self.question_label.repaint() # not ideal double checking update_q here and repaint
        