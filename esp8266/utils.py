from machine import Pin
from utime import sleep

from libs.tm1637 import TM1637

from libs.micropyserver import MicroPyServer

onboard_led = Pin(2, Pin.OUT)


def flash(pin: Pin = onboard_led, duration: float = 1.0):
    pin.on()
    sleep(duration)
    pin.off()


def init_counter(clk=5, dio=4):
    tm = TM1637(clk=Pin(clk), dio=Pin(dio))
    # all LEDS on "88:88"
    tm.write([127, 255, 127, 127])
    sleep(0.1)
    # all LEDS off
    tm.write([0, 0, 0, 0])

    return tm


def tprint(tm: TM1637, number: int):
    tm.number(number)

def catfile(fn):
    with open(fn) as f:
        print(f.read())
