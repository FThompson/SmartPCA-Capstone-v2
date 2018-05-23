import pigpio
from util.time import millis

# note: set_angle can take floats, but doing so will break sweep_angle
class Servo():
    def __init__(self, gpio, pin, rpm=25, angle=0, angle_range=180, min_pulse=500, max_pulse=2500):
        self.gpio = gpio
        self.pin = pin
        self.angle_range = angle_range
        self.min_pulse = min_pulse
        self.max_pulse = max_pulse
        self.set_speed(rpm)
        self.set_angle(angle)
        self.target_angle = angle
        self.direction = 0
        self.last_step_time = 0
        gpio.set_mode(pin, pigpio.OUTPUT)

    def set_speed(self, rpm):
        self.rpm = rpm
        self.step_delay = 60 * 1000 / self.angle_range / rpm

    def set_angle(self, angle):
        if angle < 0 or angle > self.angle_range:
            raise ValueError('angle out of range')
        self.angle = self.target_angle = angle
        pulse_range = self.max_pulse - self.min_pulse
        pulse_width = self.min_pulse + angle * pulse_range / self.angle_range
        self.gpio.set_servo_pulsewidth(self.pin, pulse_width)

    # idea: callback for what to do once sweep complete (i.e. sweep other direction)
    def sweep_angle(self, angle):
        change = angle - self.angle
        if change != 0:
            self.target_angle = angle
            self.direction = (1 if change > 0 else -1)

    def is_sweeping(self):
        return self.angle != self.target_angle

    def attach(self):
        self.set_angle(self.angle)

    def detach(self):
        self.gpio.set_servo_pulsewidth(self.pin, 0)

    def update(self):
        if self.is_sweeping():
            now = millis()
            if now - self.last_step_time > self.step_delay:
                self.last_step_time = now
                print('setting angle to ' + str(self.angle + self.direction))
                self.set_angle(self.angle + self.direction)

def main():
    from device import SERVO_PIN
    gpio = pigpio.pi()
    servo = Servo(gpio, SERVO_PIN)
    try:
        while True:
            if servo.is_sweeping():
                servo.update()
            else:
                new_rpm = int(input('RPM? Or enter 0 to detach, or -1 to attach\n'))
                if new_rpm == 0:
                    servo.detach()
                elif new_rpm == -1:
                    servo.attach()
                else:
                    servo.set_speed(new_rpm)
                    angle = int(input('What angle?\n'))
                    servo.set_angle(angle)
    finally:
        gpio.stop()

if __name__ == '__main__':
    main()
