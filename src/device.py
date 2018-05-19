import os

import pigpio
import pygame

from physical.backlight import Backlight
from physical.servo import Servo
from physical.stepper import Stepper
from prescription import Prescription
from states import State
from ui.colors import Color
from ui.scene import Scene
from ui.scenes.home import HelloLabel, DoseInfo
from ui.scenes.pain_question import PainQuestion, FaceOption
from ui.scenes.request_dose import DoseQuestion, DoseOption
from ui.scenes.dispensing import DispensingLabel

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
        self.backlight = Backlight(self.gpio, BACKLIGHT_PIN)
        self.servo = Servo(self.gpio, SERVO_PIN)
        self.stepper = Stepper(self.gpio, 512, *STEPPER_PINS)
        self.left_prescription = Prescription('Opioids', 3, 1 * 10 * 60 * 1000, True)
        self.right_prescription = Prescription('Tylenol', 2, 4 * 60 * 60 * 1000, False)
        self.selected_prescription = None
        self.desired_dose = 0
        self.setup_scenes()
        self.scene = self.scenes.get(State.HOME)
        self.state_changed = False
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
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 0, 16)
        self.screen.fill(Color.WHITE.value)
        pygame.display.update()

    def setup_scenes(self):
        pain_question = PainQuestion(self)
        self.scenes = {
            State.HOME: Scene([
                HelloLabel(),
                DoseInfo(self, self.left_prescription, Color.RIIT_BLUE.value, 34),
                DoseInfo(self, self.right_prescription, Color.RIIT_PURPLE.value, 255),
            ]),
            State.PAIN_QUESTION: Scene([
                pain_question,
                FaceOption(self, pain_question, 1, 1),
                FaceOption(self, pain_question, 2, 121),
                FaceOption(self, pain_question, 3, 241),
                FaceOption(self, pain_question, 4, 361)
            ]),
            State.REQUEST_DOSE: Scene([
                DoseQuestion(self),
                DoseOption(self, 1, 1),
                DoseOption(self, 2, 161),
                DoseOption(self, 3, 321)
            ]),
            State.DISPENSING: Scene([
                DispensingLabel(self)
            ]),
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
        self.servo.update()
        self.stepper.update()
        self.scene.update(self.screen)
        pygame.display.update()  # could optimize to only redraw prev and cur scene component rects
        self.state_changed = False

    def set_state(self, state):
        self.scene.clear(self.screen)
        self.scene = self.scenes.get(state)
        self.state_changed = True  # break draw cycle if state changed

    # brightness [0.0, 1.0]
    def set_backlight(self, brightness):
        self.backlight.set_brightness(brightness)

    def set_selected_prescription(self, prescription):
        self.selected_prescription = prescription

    # does not support distinguishing two types of medication
    def dispense(self, doses):
        pass

if __name__ == "__main__":
    device = Device()
    device.run()
