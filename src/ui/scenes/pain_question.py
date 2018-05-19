import ui.common
import ui.images
from ui.button import QuestionButton
from ui.colors import Color
from ui.component import Component
from util.time import millis
from states import State

class Question():
    def __init__(self, key, lines, ask_window):
        self.id = key
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

# bad code
def get_current_question():
    for question in QUESTIONS:
        if question.should_ask():
            return question
    return None

class PainQuestion(Component):
    def __init__(self, device):
        super().__init__(0, 0, 480, 320)
        self.device = device

    def on_repaint(self, screen):
        current_question = get_current_question()
        if current_question is None:
            self.device.set_state(State.REQUEST_DOSE)
            return
        else:
            ui.common.render_question(screen, current_question.lines)


    def on_press(self, x, y):
        pass

    def on_click(self, x, y):
        pass

    @staticmethod
    def should_ask_question(last_question_time, question_window):
        return last_question_time == 0 or millis() - last_question_time > question_window

class FaceOption(QuestionButton):
    def __init__(self, device, face, x):
        self.device = device
        self.face = face
        super().__init__(x, 191, 118, 129, Color.RIIT_LIGHT_GRAY.value)

    def get_surface(self):
        return ui.images.load_image('face{}.png'.format(self.face))

    def on_press(self, x, y):
        self.color = Color.RIIT_GRAY.value
        self.repaint()

    def on_click(self, x, y):
        self.color = Color.RIIT_LIGHT_GRAY.value
        self.repaint()
        current_question = get_current_question()
        current_question.update_ask_time()
        # TODO: record response
        print('clicked face {}'.format(self.face))
        current_question = get_current_question()
        if current_question is None:
            self.device.set_state(State.REQUEST_DOSE)
        