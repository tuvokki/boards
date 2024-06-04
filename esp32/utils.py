from machine import Pin
from utime import sleep

onboard_led = Pin(2, Pin.OUT)


def flash(pin: Pin = onboard_led, duration: float = 1.0):
    pin.on()
    sleep(duration)
    pin.off()


