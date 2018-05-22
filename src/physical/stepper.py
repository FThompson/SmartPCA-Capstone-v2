"""
Stepper motor control, adapted partially from Arduino's Stepper class
and Adafruit's Raspberry Pi stepper motor tutorial.
https://github.com/arduino-libraries/Stepper/blob/master/src/Stepper.cpp
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-10-stepper-motors

"""

import pigpio
from util.time import millis

class Stepper:
    # four-wire step signal sequence
    STEP_SIGNALS = (
        (1, 0, 1, 0),
        (0, 1, 1, 0),
        (0, 1, 0, 1),
        (1, 0, 0, 1)
    )

    def __init__(self, gpio, n_steps, pin_a1, pin_a2, pin_b1, pin_b2, rpm=25):
        self.gpio = gpio
        self.n_steps = n_steps
        self.current_step = 0
        self.target_step = 0
        self.direction = 0
        self.last_step_time = 0
        self.pin_a1 = pin_a1
        self.pin_a2 = pin_a2
        self.pin_b1 = pin_b1
        self.pin_b2 = pin_b2
        self.set_speed(rpm)
        gpio.set_mode(pin_a1, pigpio.OUTPUT)
        gpio.set_mode(pin_a2, pigpio.OUTPUT)
        gpio.set_mode(pin_b1, pigpio.OUTPUT)
        gpio.set_mode(pin_b2, pigpio.OUTPUT)

    def set_speed(self, rpm):
        self.rpm = rpm
        self.step_delay = 60 * 1000 / self.n_steps / rpm

    def set_step(self, step, is_forward):
        self.target_step = step % self.n_steps
        self.direction = (1 if is_forward else -1)

    # target_step approach does not support step inputs over n_steps
    def step(self, steps):
        if steps != 0:
            self.target_step = (self.current_step + steps) % self.n_steps
            self.direction = (1 if steps > 0 else -1)

    def send_signal(self, a1, a2, b1, b2):
        self.gpio.write(self.pin_a1, a1)
        self.gpio.write(self.pin_a2, a2)
        self.gpio.write(self.pin_b1, b1)
        self.gpio.write(self.pin_b2, b2)

    def is_stepping(self):
        return self.current_step != self.target_step

    def update(self):
        if self.is_stepping():
            now = millis()
            if now - self.last_step_time > self.step_delay:
                self.last_step_time = now
                if self.direction == 1:
                    self.current_step += 1
                    if self.current_step == self.n_steps:
                        self.current_step = 0
                else:
                    if self.current_step == 0:
                        self.current_step = self.n_steps
                    self.current_step -= 1
                signal = Stepper.STEP_SIGNALS[self.current_step % 4]
                self.send_signal(*signal)

def main():
    coil_pin_a1 = 4
    coil_pin_a2 = 17
    coil_pin_b1 = 27
    coil_pin_b2 = 22
    gpio = pigpio.pi()
    stepper = Stepper(gpio, 512, coil_pin_a1, coil_pin_a2, coil_pin_b1, coil_pin_b2)
    try:
        while True:
            if stepper.is_stepping():
                stepper.update()
            else:
                new_rpm = int(input('RPM?\n'))
                stepper.set_speed(new_rpm)
                number_of_steps = int(input('How many steps?\n'))
                stepper.step(number_of_steps)
    finally:
        gpio.stop()

if __name__ == '__main__':
    main()
