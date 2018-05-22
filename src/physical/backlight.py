import pigpio

class Backlight():
    def __init__(self, gpio, pin, brightness=1.0):
        self.gpio = gpio
        self.pin = pin
        gpio.set_mode(pin, pigpio.OUTPUT)
        gpio.set_PWM_frequency(pin, 1000)
        gpio.set_PWM_range(pin, 1023)
        self.set_brightness(brightness)

    # brightness [0.0, 1.0]
    def set_brightness(self, brightness):
        self.brightness = brightness
        print('setting brightness to {}'.format(brightness))
        self.gpio.set_PWM_dutycycle(self.pin, brightness * 1023)
