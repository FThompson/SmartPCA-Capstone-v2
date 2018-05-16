import os
import pygame
from ui.colors import Color
import RPi.GPIO as GPIO  # pylint: disable=import-error

FRAME_BUFFER = '/dev/fb1'
SCREEN_SIZE = (480, 320)

class Device:
    def __init__(self):
        os.putenv('SDL_FBDEV', FRAME_BUFFER)
        pygame.init()
        self.lcd = pygame.display.set_mode(SCREEN_SIZE)
        self.lcd.fill(Color.RIIT_BLUE.value)
        pygame.mouse.set_visible(False)
        GPIO.setmode(GPIO.BOARD)
        pygame.display.update()

    def __del__(self):
        GPIO.cleanup()

    def update(self):
        pass

if __name__ == '__main__':
    device = Device()
    while True:
        device.update()
