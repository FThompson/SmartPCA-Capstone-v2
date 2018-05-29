from util.time import millis

class Dispenser():
    def __init__(self, capacity, count, servo, stepper, slots=16, servo_start=0, servo_end=80,
                 servo_wait=1000):
        self.count = count
        self.servo = servo
        self.stepper = stepper
        self.slots = slots
        self.capacity = capacity
        self.slot_capacity = capacity // (slots - 1)
        self.steps_per_slot = stepper.n_steps // slots
        self.servo_start = servo_start
        self.servo_end = servo_end
        self.last_servo_time = 0
        self.servo_wait = servo_wait
        self.number_to_dispense = 0

    def dispense(self, count):
        self.number_to_dispense = count

    def is_dispensing(self):
        return self.number_to_dispense > 0

    def update(self):
        if not self.is_stepper_lined_up():
            if not self.stepper.is_stepping():
                self.stepper.step(self.steps_per_slot)
            else:
                self.stepper.update()
        else:
            now = millis()
            if now - self.last_servo_time > self.servo_wait:
                self.last_servo_time = now
                if self.servo.angle == self.servo_start:
                    self.servo.set_angle(self.servo_end)
                elif self.servo.angle == self.servo_end:
                    self.servo.set_angle(self.servo_start)
                    self.number_to_dispense -= 1
                    self.count -= 1

    def get_required_step(self):
        used = self.capacity - self.count
        slots_used = used // self.slot_capacity
        return (slots_used + 1) * self.steps_per_slot

    def is_stepper_lined_up(self):
        return self.get_required_step() == self.stepper.current_step
