import subprocess
import pygame
import ui.common
import ui.fonts as fonts
from ui.colors import Color
from ui.component import Component

# TODO: implement general option base class with icons
# TODO: implement RX Info, Settings, Contact doctor

class ShutdownOption(Component):
    def __init__(self, device):
        super().__init__(33, 92, 414, 47)
        self.device = device
        self.color = Color.RIIT_LIGHT_GRAY.value

    def on_repaint(self, screen):
        pygame.draw.rect(screen, self.color, self.bounds())
        font = fonts.get_font(fonts.FontType.ROBOTO_MEDIUM.value, 24)
        text = font.render("Shutdown", True, Color.BLACK.value, self.color)
        centered_rect = ui.common.center(text, *self.bounds())
        screen.blit(text, centered_rect)

    def on_press(self, x, y):
        self.color = Color.RIIT_GRAY.value
        self.repaint()

    def on_click(self, x, y):
        self.color = Color.RIIT_LIGHT_GRAY.value
        self.repaint()
        print('requested shutdown')
        subprocess.run('sudo shutdown -h now', shell=True)
