import os
from enum import Enum

import pigpio
import pygame

from prescription import Prescription
from physical.backlight import Backlight
from physical.servo import Servo
from physical.stepper import Stepper
from ui.colors import Color
from ui.scene import Scene
from ui.scenes.home import HelloLabel

SCREEN_SIZE = (480, 320)
EVENT_TYPES = (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP)

# IMPORTANT: do not use BCM pins 7, 8, 9, 10, 11, 24, 25 as they are used by the screen
BACKLIGHT_PIN = 18
SERVO_PIN = 2
STEPPER_PINS = (4, 17, 27, 22)

class State(Enum):
    HOME = 1
    PAIN_QUESTION = 2
    REQUEST_DOSE = 3
    DISPENSING = 4
    OVERRIDE_DOSE = 5
    OVERRIDE_REASON = 6
    MENU = 7
    SETTINGS = 8
    PRESCRIPTION = 9
    CONTACT = 10

class Device:
    def __init__(self):
        print('Initializing pigpio... ')
        self.gpio = pigpio.pi()
        print('Done.')
        print('Initializing pygame... ')
        self.setup_pygame()
        print('Done.')
        print('Initializing components... ')
        self.backlight = Backlight(self.gpio, BACKLIGHT_PIN)
        self.servo = Servo(self.gpio, SERVO_PIN)
        self.stepper = Stepper(self.gpio, 512, *STEPPER_PINS)
        self.left_prescription = Prescription('Opioids', 3, 1 * 10 * 60 * 1000, True)
        self.right_prescription = Prescription('Tylenol', 2, 4 * 60 * 60 * 1000, False)
        self.selected_prescription = None
        self.setup_scenes()
        self.set_state(State.HOME)
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
        pygame.event.set_allowed(EVENT_TYPES)
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.screen.fill(Color.WHITE.value)
        pygame.display.update()

    def setup_scenes(self):
        self.scenes = {
            State.HOME: Scene([
                HelloLabel()
            ]),
            State.PAIN_QUESTION: None,
            State.REQUEST_DOSE: None,
            State.DISPENSING: None,
            State.OVERRIDE_DOSE: None,
            State.OVERRIDE_REASON: None,
            State.MENU: None,
            State.SETTINGS: None,
            State.PRESCRIPTION: None,
            State.CONTACT: None
        }

    def run(self):
        print('Running.\n')
        try:
            while self.running:
                self.update()
        except KeyboardInterrupt:
            print('\nQuit requested via keyboard interrupt')
            self.running = False

    def update(self):
        # pygame.draw.circle(self.screen, Color.RIIT_PURPLE.value, pygame.mouse.get_pos(), 10, 3)
        self.servo.update()
        self.stepper.update()
        self.scene.update(self.screen)
        pygame.display.update()
        # event_queue = pygame.event.get()
        # [e.pos for e in event_queue]

    def set_state(self, state):
        self.scene = self.scenes.get(state)

    # brightness [0.0, 1.0]
    def set_backlight(self, brightness):
        self.backlight.set_brightness(brightness)

if __name__ == '__main__':
    device = Device()
    device.run()

def get_device():
    return device
