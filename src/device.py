import os
import pigpio
import pygame
from states import State
from physical.servo import Servo
from physical.stepper import Stepper
from ui.colors import Color
from ui.component import ComponentHandler

FRAME_BUFFER = '/dev/fb1'
SCREEN_SIZE = (480, 320)
EVENT_TYPES = (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.QUIT)

SERVO_PIN = 25
STEPPER_PINS = (4, 17, 23, 24)

class Device:
    def __init__(self):
        print('Initializing pigpio... ')
        self.gpio = pigpio.pi()
        print('Done.')
        print('Initializing pygame... ')
        self.setup_pygame()
        print('Done.')
        print('Initializing components... ')
        self.state = State.HOME
        self.servo = Servo(self.gpio, SERVO_PIN)
        self.stepper = Stepper(self.gpio, 512, *STEPPER_PINS)
        self.component_handler = ComponentHandler()
        self.running = True
        print('Done.')

    def __del__(self):
        self.gpio.stop()

    def setup_pygame(self):
        os.putenv('SDL_FBDEV', FRAME_BUFFER)
        pygame.init()
        #pygame.event.set_allowed(EVENT_TYPES)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen.fill(Color.RIIT_BLUE.value)
        pygame.mouse.set_visible(False)
        pygame.display.update()

    def run(self):
        print('Running.\n')
        while self.running:
            self.update()

    def update(self):
        if pygame.event.peek(pygame.QUIT):
            self.running = False
        else:
            self.servo.update()
            self.stepper.update()
            self.component_handler.update(self.state)

    def set_backlight(self, brightness):
        pass

if __name__ == '__main__':
    device = Device()
    device.run()
