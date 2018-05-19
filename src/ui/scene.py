import pygame
from ui.colors import Color

class Scene():
    def __init__(self, components=None):
        self.components = [] if components is None else components

    def add(self, component):
        self.components.append(component)

    def update(self, screen):
        event_queue = pygame.event.get()
        for component in self.components:
            # if device.get_device().state_changed:
            #     break
            component.paint(screen)
            for event in event_queue:
                x, y = event.pos
                if component.contains(x, y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        component.on_press(x, y)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        component.on_click(x, y)

    def clear(self, screen):
        for component in self.components:
            pygame.draw.rect(screen, Color.WHITE.value, component.bounds())
