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
