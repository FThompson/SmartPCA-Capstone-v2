import math
import pygame
import pygame.gfxdraw
import ui.common
import ui.fonts as fonts
from ui.colors import Color
from ui.component import Component
from states import State
from util.time import millis

class HelloLabel(Component):
    def __init__(self):
        super().__init__(105, 25, 270, 29)

    def on_repaint(self, screen):
        font = fonts.get_font(fonts.FontType.ROBOTO_LIGHT.value, 24)
        text = font.render('Hello.', True, Color.RIIT_DARKER_GRAY.value, Color.WHITE.value)
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
        self.displaying_ready = True
        self.last_repaint_time = 0
        self.repaint_delay = 1000  # repaint once per second

    def on_repaint(self, screen):
        pygame.draw.rect(screen, Color.WHITE.value, (self.dx(14), self.dy(6), 162, 188)) # clear
        pygame.draw.rect(screen, self.border_color, self.bounds(), 1)
        doses = self.prescription.get_available_doses()
        if doses == self.prescription.max_dose:
            self.displaying_ready = True
            pygame.gfxdraw.aacircle(screen, self.dx(95), self.dy(87), 75, self.color)
            pygame.gfxdraw.filled_circle(screen, self.dx(95), self.dy(87), 75, self.color)
            ready_font = fonts.get_font(fonts.FontType.ROBOTO_LIGHT.value, 36)
            text = ready_font.render("Ready", True, Color.WHITE.value, self.color)
            centered_rect = ui.common.center(text, self.x, self.dy(12), self.w, 150)
            screen.blit(text, centered_rect)
        else:
            self.displaying_ready = False
            self.draw_progress_circle(screen)
        self.draw_dose_dots(screen, doses)
        label_font = fonts.get_font(fonts.FontType.ROBOTO_MEDIUM.value, 24)
        text = label_font.render(self.prescription.label.upper(), True, Color.RIIT_DARK_GRAY.value,
                                 Color.WHITE.value)
        centered_rect = ui.common.center(text, self.x, self.dy(194), self.w, 24)
        screen.blit(text, centered_rect)

    def on_press(self, x, y):
        self.border_color = Color.RIIT_DARK_GRAY.value
        self.repaint()

    def on_click(self, x, y):
        self.border_color = Color.RIIT_GRAY.value
        self.device.set_selected_prescription(self.prescription)
        if self.device.has_pain_question():
            self.device.set_state(State.PAIN_QUESTION)
        else:
            self.device.set_state(State.REQUEST_DOSE)

    def needs_repaint(self):
        if not self.displaying_ready: # displaying progress, so repaint often
            now = millis()
            if now - self.last_repaint_time > self.repaint_delay:
                self.last_repaint_time = now
                return True
        return super().needs_repaint()

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

    # need to break this monster down
    # should prob rewrite fonts to have a render function on font enum type with centering
    # TODO: write custom anti alias arc code
    def draw_progress_circle(self, screen):
        x = self.dx(20)
        y = self.dy(12)
        pygame.gfxdraw.aacircle(screen, x + 75, y + 75, 75, Color.RIIT_GRAY.value)
        progress = 1 - self.prescription.get_time_until_next_dose() / self.prescription.dose_window
        rads = 2 * math.pi * progress
        end = (1 * math.pi / 2)
        start = end - rads
        pygame.draw.arc(screen, self.color, (x - 2, y - 2, 154, 154), start, end, 4)
        dot_x = round(75 * math.cos(start)) + 75
        dot_y = round(75 * -math.sin(start)) + 75
        pygame.gfxdraw.aacircle(screen, x + dot_x, y + dot_y, 5, self.color)
        pygame.gfxdraw.filled_circle(screen, x + dot_x, y + dot_y, 5, self.color)
        number, unit = self.prescription.format_time_until_next_dose()
        number_font = fonts.get_font(fonts.FontType.ROBOTO_LIGHT.value, 64)
        number_text = number_font.render(str(number), True, Color.RIIT_DARK_GRAY.value,
                                         Color.WHITE.value)
        number_centered_rect = ui.common.center(number_text, self.x, y + 29, self.w, 64)
        screen.blit(number_text, number_centered_rect)
        unit_font = fonts.get_font(fonts.FontType.ROBOTO_MEDIUM.value, 18)
        unit_text = unit_font.render(unit, True, Color.RIIT_DARK_GRAY.value, Color.WHITE.value)
        unit_centered_rect = ui.common.center(unit_text, self.x, y + 100, self.w, 18)
        screen.blit(unit_text, unit_centered_rect)
