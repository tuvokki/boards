from machine import PWM, Pin

from libs import RGBLed
from libs.servo import Servo
from utils import flash

flash()

myRGB = RGBLed(23, 22, 21)
motor = Servo(pin=15)

motor.move(90)  # start servo à 90°
pwm = PWM(Pin(18, Pin.OUT))
