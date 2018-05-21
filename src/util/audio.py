from enum import Enum

import pygame
import util.resources as resources

class Sample(Enum):
    DISPENSE = 'chime.wav'

    def __init__(self, value):
        self.sound = None

    def play(self):
        if self.sound is None:
            file_path = resources.get_resource_path(self.value)
            self.sound = pygame.mixer.Sound(file_path)
        self.sound.play()

def set_volume(volume):
    for s in Sample:
        s.sound.set_volume(volume)
