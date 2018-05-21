import ui.common
import ui.fonts as fonts
from ui.colors import Color
from ui.component import Component

class DispensingLabel(Component):
    def __init__(self, device):
        super().__init__(0, 0, 480, 320)
        self.device = device

    def on_repaint(self, screen):
        font = fonts.get_font(fonts.FontType.ROBOTO_MEDIUM.value, 36)
        medication = self.device.selected_prescription.label
        label = 'Dispensing {} {}'.format(self.device.desired_dose, medication)
        text = font.render(label, True, Color.RIIT_DARKER_GRAY.value, Color.WHITE.value)
        centered_rect = ui.common.center(text, *self.bounds())
        screen.blit(text, centered_rect)

    def on_press(self, x, y):
        pass

    def on_click(self, x, y):
        pass
