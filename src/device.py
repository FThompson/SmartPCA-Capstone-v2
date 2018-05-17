import os
import pigpio
import pygame
from ui.colors import Color

FRAME_BUFFER = '/dev/fb1'
SCREEN_SIZE = (480, 320)

class Device:
    def __init__(self):
        self.gpio = pigpio.pi()
        os.putenv('SDL_FBDEV', FRAME_BUFFER)
        pygame.init()
        self.lcd = pygame.display.set_mode(SCREEN_SIZE)
        self.lcd.fill(Color.RIIT_BLUE.value)
        pygame.mouse.set_visible(False)
        pygame.display.update()

    def __del__(self):
        self.gpio.stop()

    def update(self):
        pass

if __name__ == '__main__':
    device = Device()
    while True:
        device.update()
