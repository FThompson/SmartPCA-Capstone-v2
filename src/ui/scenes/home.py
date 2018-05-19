import pygame
import pygame.gfxdraw
import ui.common
import ui.fonts as fonts
from ui.colors import Color
from ui.component import Component
from states import State

class HelloLabel(Component):
    def __init__(self):
        super().__init__(105, 25, 270, 29)

    def on_repaint(self, screen):
        font = fonts.get_font(fonts.FontType.ROBOTO_LIGHT.value, 24)
        text = font.render("Hello.", True, Color.RIIT_DARKER_GRAY.value, Color.WHITE.value)
        centered_rect = ui.common.center(text, *self.bounds())
        screen.blit(text, centered_rect)

    def on_press(self, x, y):
        pass

    def on_click(self, x, y):
        pass

class DoseInfo(Component):
    def __init__(self, device, prescription, color, x):
        super().__init__(x, 63, 190, 231)
        self.device = device
        self.prescription = prescription
        self.color = color
        self.border_color = Color.RIIT_GRAY.value

    def on_repaint(self, screen):
        pygame.draw.rect(screen, self.border_color, self.bounds(), 1)
        doses = self.prescription.get_available_doses()
        if doses == self.prescription.max_dose:
            pygame.gfxdraw.aacircle(screen, self.dx(95), self.dy(87), 75, self.color)
            pygame.gfxdraw.filled_circle(screen, self.dx(95), self.dy(87), 75, self.color)
            ready_font = fonts.get_font(fonts.FontType.ROBOTO_LIGHT.value, 36)
            text = ready_font.render("Ready", True, Color.WHITE.value, self.color)
            centered_rect = ui.common.center(text, self.x, self.dy(12), self.w, 150)
            screen.blit(text, centered_rect)
        else:
            self.draw_progress_circle(screen)
        self.draw_dose_dots(screen, doses)
        label_font = fonts.get_font(fonts.FontType.ROBOTO_MEDIUM.value, 24)
        text = label_font.render(self.prescription.label.upper(), True, Color.RIIT_DARK_GRAY.value,
                                 Color.WHITE.value)
        centered_rect = ui.common.center(text, self.x, self.dy(194), self.w, 24)
        screen.blit(text, centered_rect)

    def on_press(self, x, y):
        self.border_color = Color.RIIT_BLUE.value
        self.repaint()

    def on_click(self, x, y):
        self.border_color = Color.RIIT_GRAY.value
        self.device.set_selected_prescription(self.prescription)
        self.device.set_state(State.PAIN_QUESTION)

    def draw_dose_dots(self, screen, doses):
        dots_width = 10 * self.prescription.max_dose + 9 * (self.prescription.max_dose - 1)
        dots_x = self.dx(int(self.w / 2 - dots_width / 2))
        dot_y = self.dy(179)
        for i in range(self.prescription.max_dose):
            dot_x = dots_x + 5 + i * 19
            if i < doses:
                pygame.gfxdraw.aacircle(screen, dot_x, dot_y, 5, self.color)
                pygame.gfxdraw.filled_circle(screen, dot_x, dot_y, 5, self.color)
            else:
                pygame.gfxdraw.aacircle(screen, dot_x, dot_y, 5, Color.RIIT_DARK_GRAY.value)

    def draw_progress_circle(self, screen):
        pass
