import time
from machine import Pin, PWM
from ble import BLE
from lcd_i2c import init_lcd

lcd = init_lcd("Start")
time.sleep(1.0)
lcd.clear()
lcd.print("Ready")

beeper = Pin(27, Pin.OUT)
yellow_led = Pin(32, Pin.OUT)
leds = {
    "yellow": yellow_led
}


def on_rx(_val: bytes):
    val = _val.decode("utf-8")
    lcd.clear()
    if val.startswith("beep"):
        try:
            _, _duration = val.split(":")
            duration = int(_duration)
        except ValueError:
            duration = 1
        lcd.print(f"Beep {duration} sec.")
        beeper.value(1)
        time.sleep(duration)
        beeper.value(0)
    elif val.startswith("led"):
        _, _led, action = val.split(":")
        lcd.print(f"{_led} {action}")
        led = leds[_led]
        if action == "on":
            led.value(1)
        if action == "off":
            led.value(0)
        if action == "toggle":
            led.value(not led.value())
    elif val == "wait":
        lcd.print("Waiting...")
        time.sleep(1)
    else:
        lcd.print(val)


ble = BLE("Hello32")
ble.on_write(on_rx)
