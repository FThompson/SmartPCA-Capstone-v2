import time
from abc import ABC, abstractmethod

def millis():
    return int(round(time.time() * 1000))

# class NonBlockingAction(ABC):
#     def __init__(self, action, done_condition):
#         self.action = action
#         self.done_condition = done_condition

#     def check(self):
#         if self.done_condition():
#             self.done_action()
