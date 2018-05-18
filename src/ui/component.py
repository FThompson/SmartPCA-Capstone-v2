import pygame
from abc import ABC, abstractmethod

class Component(ABC):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @abstractmethod
    def get_valid_states(self):
        pass

    @abstractmethod
    def on_paint(self):
        pass

    @abstractmethod
    def on_press(self, x, y):
        pass

    @abstractmethod
    def on_click(self, x, y):
        pass

    def contains(self, x, y):
        return x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h

    def dx(self, x):
        return x + self.x

    def dy(self, y):
        return y + self.y

class ComponentHandler():
    def __init__(self):
        self.components = []

    def add(self, component):
        self.components.append(component)

    def update(self, state):
        event_queue = pygame.event.get()
        mouse_events = [e for e in event_queue if e.type != pygame.QUIT]
        for e in mouse_events:
            print('mouse event type {} at {},{}'.format(e.type, e.pos[0], e.pos[1]))
        for component in self.components:
            if state in component.get_valid_states():
                component.paint()
                for event in mouse_events:
                    if component.contains(event.pos[0], event.pos[1]):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            component.on_press()
                        elif event.type == pygame.MOUSEBUTTONUP:
                            component.on_click()
