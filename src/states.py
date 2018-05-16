from enum import Enum

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
