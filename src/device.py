import os

import pigpio
import pygame

import util.audio as audio
from physical.backlight import Backlight
from physical.servo import Servo
from physical.stepper import Stepper
from prescription import Prescription
from states import State
from ui.colors import Color
from ui.back_button import BackButton
from ui.menu_button import MenuButton
from ui.scene import Scene
from ui.scenes.dispensing import DispensingLabel
from ui.scenes.home import DoseInfo, HelloLabel
from ui.scenes.override_dose import OverrideOption, OverrideQuestion
from ui.scenes.pain_question import FaceOption, PainQuestion, PainQuestionLabel
from ui.scenes.request_dose import DoseOption, DoseQuestion
from ui.scenes.override_reason import OverrideLabel, OverrideReasonOption

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
        self.stepper = Stepper(self.gpio, 512, *STEPPER_PINS, rpm=50)
        self.left_prescription = Prescription('Opioids', 3, 1 * 2 * 60 * 1000, True)
        self.right_prescription = Prescription('Tylenol', 2, 4 * 60 * 60 * 1000, False)
        self.selected_prescription = None
        self.desired_dose = 0
        self.pain_question = PainQuestion.get_current_question()
        self.setup_scenes()
        self.state = State.HOME
        self.last_state = self.state
        self.scene = self.scenes.get(self.state)
        self.running = True
        self.dispensing = False
        print('Done.')

    def __del__(self):
        #self.backlight.set_brightness(0)
        self.gpio.stop()

    def setup_pygame(self):
        os.putenv('SDL_FBDEV', '/dev/fb1')
        os.putenv('SDL_MOUSEDRV', 'TSLIB')
        os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
        # pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
        pygame.init()
        # pygame.mixer.init()
        pygame.event.set_allowed(EVENT_TYPES)
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 0, 16)
        self.screen.fill(Color.WHITE.value)
        pygame.display.update()

    def setup_scenes(self):
        back_button = BackButton(self)
        pain_question = PainQuestionLabel(self)
        self.scenes = {
            State.HOME: Scene([
                HelloLabel(),
                DoseInfo(self, self.left_prescription, Color.RIIT_BLUE.value, 34),
                DoseInfo(self, self.right_prescription, Color.RIIT_PURPLE.value, 255),
                MenuButton(self)
            ]),
            State.PAIN_QUESTION: Scene([
                pain_question,
                FaceOption(self, 1, 1),
                FaceOption(self, 2, 121),
                FaceOption(self, 3, 241),
                FaceOption(self, 4, 361),
                back_button
            ]),
            State.REQUEST_DOSE: Scene([
                DoseQuestion(self),
                DoseOption(self, 1, 1),
                DoseOption(self, 2, 161),
                DoseOption(self, 3, 321),
                back_button
            ]),
            State.DISPENSING: Scene([
                DispensingLabel(self)
            ]),
            State.OVERRIDE_DOSE: Scene([
                OverrideQuestion(self),
                OverrideOption(self, 'YES', State.OVERRIDE_REASON, 1),
                OverrideOption(self, 'NO', State.HOME, 241),
                back_button
            ]),
            State.OVERRIDE_REASON: Scene([
                OverrideLabel(),
                OverrideReasonOption(self, 'I am in pain right now.', 1),
                OverrideReasonOption(self, 'I lost/cannot find the pill', 2),
                OverrideReasonOption(self, 'Pill did not dispense.', 3),
                back_button
            ]),
            State.MENU: Scene([
                back_button
            ]),
            State.SETTINGS: Scene([
                back_button
            ]),
            State.PRESCRIPTION: Scene([
                back_button
            ]),
            State.CONTACT: Scene([
                back_button
            ])
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
        # if self.dispensing:
        #     return  # smooths out stepper motor motion
        self.scene.update(self.screen)
        pygame.display.update()  # could optimize to only redraw prev and cur scene component rects

    def set_state(self, state):
        audio.Sample.DISPENSE.play()
        print('setting state to {}'.format(state))
        self.last_state = state
        self.scene.clear(self.screen)
        self.scene = self.scenes.get(state)
        self.scene.repaint()
        self.state = state

    # brightness [0.0, 1.0]
    def set_backlight(self, brightness):
        self.backlight.set_brightness(brightness)

    def set_selected_prescription(self, prescription):
        self.selected_prescription = prescription

    def has_pain_question(self):
        self.pain_question = PainQuestion.get_current_question()
        return self.pain_question is not None

    # does not support distinguishing two types of medication
    def dispense(self, doses):
        self.set_state(State.HOME)
        #self.dispensing = True
        pass

if __name__ == "__main__":
    device = Device()
    device.run()
