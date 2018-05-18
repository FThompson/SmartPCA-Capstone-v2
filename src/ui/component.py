from abc import ABC, abstractmethod

class Component(ABC):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.repainting = True

    @abstractmethod
    def on_repaint(self, screen):
        pass

    @abstractmethod
    def on_press(self, x, y):
        pass

    @abstractmethod
    def on_click(self, x, y):
        pass

    def paint(self, screen):
        if self.needs_repaint():
            self.on_repaint(screen)
            self.repainting = False

    # custom components can override if needing more frequent repaint
    def needs_repaint(self):
        return self.repainting

    def repaint(self):
        self.repainting = True

    def bounds(self):
        return (self.x, self.y, self.w, self.h)

    def contains(self, x, y):
        return x >= self.x and x <= self.x + self.w and y >= self.y and y <= self.y + self.h

    def dx(self, x):
        return x + self.x

    def dy(self, y):
        return y + self.y
