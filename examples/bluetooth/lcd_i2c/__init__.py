from machine import I2C, Pin

from .lcd_i2c import LCD


def init_lcd(message: str = "Hello World!", clear_screen: bool = True) -> LCD:
    # PCF8574 on 0x50
    I2C_ADDR = 0x27  # DEC 39, HEX 0x27
    NUM_ROWS = 4
    NUM_COLS = 20

    # define custom I2C interface, default is 'I2C(0)'
    # check the docs of your device for further details and pin infos
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=800000)
    _lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)

    _lcd.set_start_state()
    if clear_screen:
        _lcd.clear()
    if message != "":
        _lcd.print(message)
    return _lcd
