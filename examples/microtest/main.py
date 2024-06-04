import time
from machine import I2C, Pin, SoftI2C

from tm1637 import TM1637
from lcd_i2c import LCD
from adxl345 import ADXL345


def blink_led(led: Pin, times: int = 3, interval: float = 1.0):
    for _ in range(times):
        led.on()
        time.sleep(interval)


def blink_display(display: TM1637, times: int = 3, interval: float = 1.0):
    for _ in range(times):
        # all LEDS on "88:88"
        display.write([127, 255, 127, 127])
        time.sleep(interval)
        # all LEDS off
        display.write([0, 0, 0, 0])
        time.sleep(interval)


def init_lcd(message: str = "Hello World!") -> LCD:
    # PCF8574 on 0x50
    I2C_ADDR = 0x27  # DEC 39, HEX 0x27
    NUM_ROWS = 2
    NUM_COLS = 16

    # define custom I2C interface, default is 'I2C(0)'
    # check the docs of your device for further details and pin infos
    i2c = I2C(0, scl=Pin(26), sda=Pin(25), freq=800000)
    lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)

    lcd.begin()
    lcd.print(message)
    return lcd


def init_accel() -> ADXL345:
    # Define I2C pins
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

    # Initialize ADXL345
    accel = ADXL345(i2c)
    return accel


print("STARTING MAIN")
led14 = Pin(14, Pin.OUT)

# do_connect(led14)

tm = TM1637(clk=Pin(5), dio=Pin(4))
blink_display(tm, 1, 0.5)

led14.on()
# for i in range(10):
#     for j in range(10):
#         tm.numbers(i, j)
#         time.sleep(0.1)
# led14.off()

lcdo = init_lcd("We gaan wat dingen meten!!")
time.sleep(3)
# accelo = init_accel()
# # Read accelerometer data
# while True:
#     x, y, z = accelo.read()
#     acc_data = f"x = {x}, y = {y}, z = {z}"
#     print(acc_data)
#     lcdo.clear()
#     # lcdo.print(acc_data)
#     lcdo.set_cursor(0,0)
#     lcdo.print(f"x = {x}")
#     lcdo.set_cursor(0,1)
#     lcdo.print(f"y = {y}")
#     lcdo.set_cursor(0,3)
#     lcdo.print(f"z = {z}")
#     time.sleep_ms(10)


# blink_display(tm, interval=0.1)

# app.run(debug=True)
