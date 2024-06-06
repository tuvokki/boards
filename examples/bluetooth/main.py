import time

from ble import BLE
from lcd_i2c import init_lcd

print("Finished main")
ble = BLE("Hello32")
lcd = init_lcd("Start")
time.sleep(1.0)
lcd.clear()
lcd.print("Ready")
