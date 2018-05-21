import ui.common
from ui.button import QuestionButton
from ui.colors import Color
from ui.component import Component
import ui.fonts as fonts

class OverrideQuestion(Component):
    def __init__(self, device):
        super().__init__(0, 0, 480, 229)
        self.device = device

    def on_repaint(self, screen):
        lines = (
            'Oops, next dose is in',
            '{} {}. Would'.format(*self.device.selected_prescription.format_time_until_next_dose()),
            'you like to override?'
        )
        ui.common.render_question(screen, lines)

    def on_press(self, x, y):
        pass

    def on_click(self, x, y):
        pass

class OverrideOption(QuestionButton):
    def __init__(self, device, option, action_state, x):
        super().__init__(x, 229, 238, 91, Color.RIIT_LIGHT_GRAY.value)
        self.device = device
        self.option = option
        self.action_state = action_state

    def get_surface(self):
        font = fonts.get_font(fonts.FontType.ROBOTO_MEDIUM.value, 36)
        return font.render(self.option, True, Color.BLACK.value, self.color)

    def on_press(self, x, y):
        self.color = Color.RIIT_GRAY.value
        self.repaint()

    def on_click(self, x, y):
        self.color = Color.RIIT_LIGHT_GRAY.value
        self.repaint()
        print('chose {} to override'.format(self.option))
        self.device.set_state(self.action_state)
