import pygame

class Scene():
    def __init__(self, state):
        self.state = state
        self.components = []

    def add(self, component):
        self.components.append(component)

    def get_state(self):
        return self.state

    def update(self):
        event_queue = pygame.event.get()
        for e in event_queue:
            print('mouse event type {} at {},{}'.format(e.type, e.pos[0], e.pos[1]))
        for component in self.components:
            component.paint()
            for event in event_queue:
                x, y = event.pos
                if component.contains(x, y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        component.on_press()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        component.on_click()