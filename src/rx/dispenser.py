import time
from abc import ABC, abstractmethod

# class Dispenser(ABC):
class Dispenser():
    def __init__(self, capacity, count, servo, stepper, slots=16, servo_start=0, servo_end=120):
        self.count = count
        self.servo = servo
        self.stepper = stepper
        self.slots = slots
        self.slot_capacity = capacity / (slots - 1)
        self.step_angle = stepper.n_steps / slots
        self.servo_start = servo_start
        self.servo_end = servo_end

    # @abstractmethod
    def dispense(self, count):
        current_slot_count = self.count % self.slot_capacity
        if current_slot_count == 0 or self.stepper.current_step == 0:
            self.stepper.step(self.step_angle)
            while self.stepper.is_stepping():
                self.stepper.update()
            time.sleep(0.25)
        self.servo.set_angle(self.servo_end)
        time.sleep(1)
        self.servo.set_angle(self.servo_start)
        time.sleep(1)
        self.count -= 1
        if count > 1:
            self.dispense(count - 1)

    # def update(self):
    #     current_slot_count = self.count % self.slot_capacity
    #     if current_slot_count == 0:
    #         self.stepper.step(self.step_angle)

# class Dispenser2():
#     def __init__(self, capacity1, capacity2, count1, count2, servo, stepper, slots=16, servo_start=0, servo_end=120):
#         self.capacity = capacity
#         self.count = count
#         self.servo = servo
#         self.stepper = stepper
#         self.slots = slots
#         self.slot_capacity = capacity / (slots - 1)
#         self.step_angle = stepper.n_steps / slots
#         self.servo_start = servo_start
#         self.servo_end = servo_end
