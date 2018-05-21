from enum import Enum

import pygame

class Sample(Enum):
    DISPENSE = 'chime.wav'

    def __init__(self, file_name):
        self.sound = pygame.mixer.Sound(file_name)

    def play(self):
        self.sound.play()

def set_volume(volume):
    for s in Sample:
        s.sound.set_volume(volume)
