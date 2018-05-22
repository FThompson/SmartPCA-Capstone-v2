from enum import Enum

import time

import pygame
import util.resources as resources

class Sample(Enum):
    DISPENSE = 'chime.wav'

    def __init__(self, _):
        self.sound = None
        self.volume = 1.0

    def play(self):
        if self.sound is None:
            file_path = resources.get_resource_path(self.value)
            self.sound = pygame.mixer.Sound(file_path)
        self.sound.set_volume(self.volume)
        self.sound.play()

    def set_volume(self, volume):
        self.volume = volume

def set_volume(volume):
    for s in Sample:
        s.sound.set_volume(volume)

def main():
    pygame.init()
    while True:
        if Sample.DISPENSE.volume > 0.4:
            Sample.DISPENSE.volume -= 0.2
        print('playing sample at {}'.format(Sample.DISPENSE.volume))
        Sample.DISPENSE.play()
        time.sleep(10)

if __name__ == '__main__':
    main()
