import os
import pigpio
import pygame
from states import State
from physical.backlight import Backlight
from physical.servo import Servo
from physical.stepper import Stepper
from ui.colors import Color
from ui.component import ComponentHandler

SCREEN_SIZE = (480, 320)
EVENT_TYPES = (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)

# IMPORTANT: do not use BCM pins 7, 8, 9, 10, 11, 24, 25 as they are used by the screen
BACKLIGHT_PIN = 18
SERVO_PIN = 2
STEPPER_PINS = (4, 17, 27, 22)

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
        self.backlight = Backlight(self.gpio, BACKLIGHT_PIN)
        self.servo = Servo(self.gpio, SERVO_PIN)
        self.stepper = Stepper(self.gpio, 512, *STEPPER_PINS)
        self.component_handler = ComponentHandler()
        self.running = True
        print('Done.')

    def __del__(self):
        #self.backlight.set_brightness(0)
        self.gpio.stop()

    def setup_pygame(self):
        os.putenv('SDL_FBDEV', '/dev/fb1')
        os.putenv('SDL_MOUSEDRV', 'TSLIB')
        os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
        pygame.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 40)
        pygame.event.set_allowed(EVENT_TYPES)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen.fill(Color.RIIT_BLUE.value)
        pygame.draw.rect(self.screen, Color.RIIT_GREEN.value, (5, 5, 470, 310), 4)
        textsurface = myfont.render('Some Text hello world', False, (0, 0, 0))
        self.screen.blit(textsurface,(0,0))
        pygame.mouse.set_visible(False)
        pygame.display.update()

    def run(self):
        print('Running.\n')
        try:
            while self.running:
                self.update()
        except KeyboardInterrupt:
            print('Quit requested via keyboard interrupt')
            self.running = False

    def update(self):
        pygame.draw.circle(self.screen, Color.RIIT_PURPLE.value, pygame.mouse.get_pos(), 10, 3)
        pygame.display.update()
        self.servo.update()
        self.stepper.update()
        self.component_handler.update(self.state)

    def set_backlight(self, brightness):
        self.backlight.set_brightness(brightness)

if __name__ == '__main__':
    device = Device()
    device.run()

def get_device():
    return device
