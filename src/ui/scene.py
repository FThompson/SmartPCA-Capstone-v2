import pygame

class Scene():
    def __init__(self, components=None):
        self.components = [] if components is None else components

    def add(self, component):
        self.components.append(component)

    def repaint(self):
        for component in self.components:
            component.repaint()

    def update(self, screen):
        event_queue = pygame.event.get()
        for component in self.components:
            # if device.get_device().state_changed:
            #     break
            component.paint(screen)
            for event in event_queue:
                x, y = event.pos
                if component.contains(x, y):
                    # TODO: add press/click logic to discern click from mouseup
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        component.on_press(x, y)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        component.on_click(x, y)

    def clear(self, screen):
        for component in self.components:
            component.clear(screen)
