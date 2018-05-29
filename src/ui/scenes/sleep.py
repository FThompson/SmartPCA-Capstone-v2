from ui.component import Component

class SleepScreen(Component):
    def __init__(self, device):
        super().__init__(0, 0, 480, 320)
        self.device = device

    def on_repaint(self, screen):
        pass

    def on_press(self, x, y):
        # turn on screen, go to prev state
        pass

    def on_click(self, x, y):
        pass
