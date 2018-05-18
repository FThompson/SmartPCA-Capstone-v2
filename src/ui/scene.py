import pygame

class Scene():
    def __init__(self, components=None):
        self.components = [] if components is None else components

    def add(self, component):
        self.components.append(component)

    def update(self, screen):
        event_queue = pygame.event.get()
        # for e in event_queue:
        #     print('mouse event type {} at {},{}'.format(e.type, e.pos[0], e.pos[1]))
        for component in self.components:
            component.paint(screen)
            for event in event_queue:
                x, y = event.pos
                if component.contains(x, y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        component.on_press(x, y)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        component.on_click(x, y)
