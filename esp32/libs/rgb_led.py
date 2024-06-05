# rgb led lib

from machine import PWM, Pin
import utime


def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


class RGBLed:
    anode = 'anode'
    cathode = 'cathode'

    def __init__(self,
                 red_pin, green_pin, blue_pin,
                 ledType='anode',
                 currentValueR=0, currentValueG=0, currentValueB=0):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        self.ledType = ledType
        self.currentValueR = currentValueR
        self.currentValueG = currentValueG
        self.currentValueB = currentValueB
        self.setColor(currentValueR, currentValueG, currentValueB)

    def show(self):
        print("Led Type:", self.ledType)
        print(f"Red({self.red_pin}): {self.currentValueR}")
        print(f"Green({self.green_pin}): {self.currentValueG}")
        print(f"Blue({self.blue_pin}): {self.currentValueB}")

    def setColor(self, r, g, b):
        if self.ledType == 'anode':
            self.currentValueR = r
            self.currentValueG = g
            self.currentValueB = b

            r = convert(r, 0, 255, 65534, 0)
            g = convert(g, 0, 255, 65534, 0)
            b = convert(b, 0, 255, 65534, 0)
            red_pin_pwm = PWM(Pin(self.red_pin))
            green_pin_pwm = PWM(Pin(self.green_pin))
            blue_pin_pwm = PWM(Pin(self.blue_pin))
            red_pin_pwm.duty_u16(r)
            green_pin_pwm.duty_u16(g)
            blue_pin_pwm.duty_u16(b)
        elif self.ledType == 'cathode':
            self.currentValueR = r
            self.currentValueG = g
            self.currentValueB = b

            r = convert(r, 0, 255, 0, 65534)
            g = convert(g, 0, 255, 0, 65534)
            b = convert(b, 0, 255, 0, 65534)
            red_pin_pwm = PWM(Pin(self.red_pin))
            green_pin_pwm = PWM(Pin(self.green_pin))
            blue_pin_pwm = PWM(Pin(self.blue_pin))
            red_pin_pwm.duty_u16(r)
            green_pin_pwm.duty_u16(g)
            blue_pin_pwm.duty_u16(b)

    def off(self):
        self.setColor(0, 0, 0)

    def red(self):
        self.setColor(255, 0, 0)

    def green(self):
        self.setColor(0, 255, 0)

    def blue(self):
        self.setColor(0, 0, 255)

    def white(self):
        self.setColor(255, 255, 255)

    def yellow(self):
        self.setColor(255, 255, 0)

    def magenta(self):
        self.setColor(255, 0, 255)

    def cyan(self):
        self.setColor(0, 255, 255)

    def slowSet(self, r, g, b, delay=0.01):
        rStep = 0
        gStep = 0
        bStep = 0
        if r > self.currentValueR:
            rStep = 1
        else:
            rStep -= 1

        if g > self.currentValueG:
            gStep = 1
        else:
            gStep = -1

        if b > self.currentValueB:
            bStep = 1
        else:
            bStep = -1

        if self.ledType == 'anode':
            for i in range(self.currentValueR, r, rStep):
                x = convert(i, 0, 255, 65534, 0)
                red_pin_pwm = PWM(Pin(self.red_pin))
                red_pin_pwm.duty_u16(x)
                utime.sleep(delay)
            for i in range(self.currentValueG, g, gStep):
                x = convert(i, 0, 255, 65534, 0)
                green_pin_pwm = PWM(Pin(self.green_pin))
                green_pin_pwm.duty_u16(x)
                utime.sleep(delay)
            for i in range(self.currentValueB, b, bStep):
                x = convert(i, 0, 255, 65534, 0)
                blue_pin_pwm = PWM(Pin(self.blue_pin))
                blue_pin_pwm.duty_u16(x)
                utime.sleep(delay)

        elif self.ledType == 'cathode':
            for i in range(self.currentValueR, r, rStep):
                x = convert(i, 0, 255, 0, 65534)
                red_pin_pwm = PWM(Pin(self.red_pin))
                red_pin_pwm.duty_u16(x)
                utime.sleep(delay)
            for i in range(self.currentValueG, g, gStep):
                x = convert(i, 0, 255, 0, 65534)
                green_pin_pwm = PWM(Pin(self.green_pin))
                green_pin_pwm.duty_u16(x)
                utime.sleep(delay)
            for i in range(self.currentValueB, b, bStep):
                x = convert(i, 0, 255, 0, 65534)
                blue_pin_pwm = PWM(Pin(self.blue_pin))
                blue_pin_pwm.duty_u16(x)
                utime.sleep(delay)

        self.currentValueR = r
        self.currentValueG = g
        self.currentValueB = b
        self.setColor(r, g, b)

    def test(self):
        self.red()
        utime.sleep(0.5)
        self.green()
        utime.sleep(0.5)
        self.blue()
        utime.sleep(0.5)
        self.white()
        utime.sleep(0.5)
        self.cyan()
        utime.sleep(0.5)
        self.yellow()
        utime.sleep(0.5)
        self.magenta()
        utime.sleep(0.5)
        self.slowSet(255, 0, 0)
        utime.sleep(0.1)
        self.slowSet(0, 255, 0)
        utime.sleep(0.1)
        self.slowSet(0, 0, 255)
        utime.sleep(0.5)
        self.off()
        utime.sleep(0.2)
        self.red()
        utime.sleep(0.2)
        self.white()
        utime.sleep(0.2)
        self.blue()
        utime.sleep(0.2)
        self.off()
        utime.sleep(0.2)
        self.red()
        utime.sleep(0.2)
        self.white()
        utime.sleep(0.2)
        self.blue()
        utime.sleep(0.2)
        self.off()
