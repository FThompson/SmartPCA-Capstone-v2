import ui.common
import ui.images
from ui.button import QuestionButton
from ui.colors import Color
from ui.component import Component
import ui.fonts as fonts
from states import State

class DoseQuestion(Component):
    def __init__(self, device):
        super().__init__(0, 0, 480, 191)
        self.device = device

    def on_repaint(self, screen):
        lines = (
            'How many {} do'.format(self.device.selected_prescription.label),
            'you need right now?'
        )
        ui.common.render_question(screen, lines)

    def on_press(self, x, y):
        pass

    def on_click(self, x, y):
        pass

class DoseOption(QuestionButton):
    def __init__(self, device, position, x):
        super().__init__(x, 191, 158, 129, Color.RIIT_LIGHT_GRAY.value)
        self.device = device
        self.position = position
        self.number = position

    def get_surface(self):
        # hacky non-OOP solution to count in interest of time
        # TODO: implement solution that works for any number of dose options
        self.number = self.position
        if not self.device.selected_prescription.show_override:
            self.number -= 1
        font = fonts.get_font(fonts.FontType.ROBOTO_MEDIUM.value, 48)
        return font.render(str(self.number), True, Color.BLACK.value, self.color)

    def on_press(self, x, y):
        self.color = Color.RIIT_GRAY.value
        self.repaint()

    def on_click(self, x, y):
        self.color = Color.RIIT_LIGHT_GRAY.value
        self.repaint()
        print('requested {} {}'.format(self.number, self.device.selected_prescription.label))
        if self.number > 0:
            self.device.desired_dose = self.number
            if (self.device.selected_prescription.show_override and
                    self.number > self.device.selected_prescription.get_available_doses()):
                self.device.set_state(State.OVERRIDE_DOSE)
            else:
                self.device.set_state(State.DISPENSING)
                self.device.selected_prescription.use(self.number)
                self.device.dispense(self.number)
        else:
            self.device.set_state(State.HOME)  # zero dose selected
