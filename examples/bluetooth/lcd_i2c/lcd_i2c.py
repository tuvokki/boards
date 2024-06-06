"""
I2C LCD-Display driver for 1602 and 2004 displays controlled via I2C

LCD data sheet: https://www.sparkfun.com/datasheets/LCD/HD44780.pdf

Ported to MicroPython from
https://github.com/fdebrabander/Arduino-LiquidCrystal-I2C-library
"""
from machine import I2C
from time import sleep, sleep_ms, sleep_us

from . import const as Const


class LCD:
    """Driver for the Liquid Crystal LCD-displays that use the I2C bus"""

    def __init__(self,
                 addr: int,
                 cols: int,
                 rows: int,
                 char_size: int = 0x00,
                 i2c: I2C | None = None) -> None:
        """
        Constructs a new instance.

        :param      addr:      The LCD I2C bus address
        :param      cols:      Number of columns of the LCD
        :param      rows:      Number of rows of the LCD
        :param      char_size:  The size in dots of the LCD
        :param      i2c:       I2C object
        """
        self._addr: int = addr
        self._cols: int = cols
        self._rows: int = rows
        self._char_size: int = char_size
        self._backlight_val: int = Const.LCD_BACKLIGHT
        if i2c is None:
            # default assignment, check the docs
            self._i2c = I2C(0)
        else:
            self._i2c = i2c

        self._display_control: int = 0
        self._display_mode: int = 0
        self._display_function: int = 0
        self._cursor_position: tuple[int, int] = (0, 0)  # (x, y)

    @property
    def addr(self) -> int:
        """
        Get the LCD I2C bus address

        :returns:   LCD I2C bus address
        """
        return self._addr

    @property
    def cols(self) -> int:
        """
        Get the number of columns of the LCD

        :returns:   Number of columns of the LCD
        """
        return self._cols

    @property
    def rows(self) -> int:
        """
        Get the number of rows of the LCD

        :returns:   Number of rows of the LCD
        """
        return self._rows

    @property
    def char_size(self) -> int:
        """
        Get the size in dots of the LCD

        :returns:   Dot size of the LCD
        """
        return self._char_size

    @property
    def backlight_val(self) -> int:
        """
        Get the backlight value

        :returns:   Backlight value of the LCD
        """
        return self._backlight_val

    @property
    def cursor_position(self) -> tuple[int, int]:
        """
        Get the current cursor position

        :returns:   Cursor position as tuple(column, row) as (x, y)
        """
        return self._cursor_position

    @cursor_position.setter
    def cursor_position(self, position: tuple[int, int]) -> None:
        """
        Set the cursor position

        :param      position:  The cursor position
        """
        self.set_cursor(col=position[0], row=position[1])  # (x, y)

    def set_start_state(self) -> None:
        """
        Set the LCD-display in the correct start state

        Must be called before anything else is done
        """
        self._display_function = Const.LCD_4BITMODE | Const.LCD_1LINE | Const.LCD_5x8DOTS

        if self.rows > 1:
            self._display_function |= Const.LCD_2LINE

        # for some 1 line displays you can select a 10 pixel high font
        if (self.char_size != 0) and (self.rows == 1):
            self._display_function |= Const.LCD_5x10DOTS

        # SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
        # according to datasheet, we need at least 40ms after power rises
        # above 2.7V before sending commands. Controller can turn on way before
        # 4.5V, so we'll wait 50ms
        sleep_ms(50)

        # Now we pull both RS and R/W low to begin commands
        # reset expander and turn backlight off (Bit 8 =1)
        self._expander_write(value=self.backlight_val)
        sleep(1)

        # put the LCD into 4 bit mode
        # this is according to the Hitachi HD44780 datasheet
        # figure 24, page 46

        # we start in 8 bit mode, try to set 4 bit mode
        for _ in range(0, 3):
            self._write_4_bits(value=(0x03 << 4))
            sleep_us(4500)  # wait minimum 4.1ms

        # finally, set to 4 bit interface
        self._write_4_bits(value=(0x02 << 4))

        # set number of lines, font size, etc
        self._command(value=(Const.LCD_FUNCTIONSET | self._display_function))

        # turn the display on with no cursor or blinking default
        self._display_control = Const.LCD_DISPLAYON | Const.LCD_CURSOROFF | Const.LCD_BLINKOFF
        self.display()

        # clear it off
        self.clear()

        # Initialize to default text direction (for roman languages)
        self._display_mode = Const.LCD_ENTRYLEFT | Const.LCD_ENTRYSHIFTDECREMENT

        # set the entry mode
        self._command(value=(Const.LCD_ENTRYMODESET | self._display_mode))

        self.home()

    def clear(self) -> None:
        """
        Remove all the characters currently shown

        Next print/write operation will start from the first position on LCD-display.
        """
        # clear display and set cursor position to zero
        self._command(value=Const.LCD_CLEARDISPLAY)
        sleep_ms(2)  # this command takes a long time!
        self._cursor_position = (0, 0)  # (x, y)

    def home(self) -> None:
        """
        Set cursor to home position (0, 0)

        Next print/write operation will start from the first position on the LCD-display.
        """
        # set cursor position to zero
        self._command(value=Const.LCD_RETURNHOME)
        sleep_ms(2)  # this command takes a long time!
        self._cursor_position = (0, 0)  # (x, y)

    def no_display(self) -> None:
        """
        Turn the display off

        Do not show any characters on the LCD-display. Backlight state will
        remain unchanged. Also, all characters written on the display will
        return, when the display in enabled again.

        @see display
        """
        self._display_control &= ~Const.LCD_DISPLAYON
        self._command(value=(Const.LCD_DISPLAYCONTROL | self._display_control))

    def display(self) -> None:
        """
        Turn the display on

        Show the characters on the LCD-display, this is the normal behaviour.
        This method should only be used after no_display() has been used.
        """
        self._display_control |= Const.LCD_DISPLAYON
        self._command(value=(Const.LCD_DISPLAYCONTROL | self._display_control))

    def no_blink(self) -> None:
        """Turn the blinking cursor off"""
        self._display_control &= ~Const.LCD_BLINKON
        self._command(value=(Const.LCD_DISPLAYCONTROL | self._display_control))

    def blink(self) -> None:
        """Turn the blinking cursor on"""
        self._display_control |= Const.LCD_BLINKON
        self._command(value=(Const.LCD_DISPLAYCONTROL | self._display_control))

    def no_cursor(self) -> None:
        """Turn the underline cursor off"""
        self._display_control &= ~Const.LCD_CURSORON
        self._command(value=(Const.LCD_DISPLAYCONTROL | self._display_control))

    def cursor(self) -> None:
        """
        Turn the underline cursor on

        Cursor can blink or not blink. Use the methods @see blink and
        @see no_blink for changing the cursor blink status.
        """
        self._display_control |= Const.LCD_CURSORON
        self._command(value=(Const.LCD_DISPLAYCONTROL | self._display_control))

    def set_cursor(self, col: int, row: int) -> None:
        """
        Set the cursor

        :param      col:  The new column of the cursor
        :param      row:  The new row of the cursor
        """
        row_offsets: list[int] = [0x00, 0x40, 0x14, 0x54]

        # we count rows starting w/0
        if row > (self.rows - 1):
            row = self.rows - 1

        self._command(value=(Const.LCD_SETDDRAMADDR | (col + row_offsets[row])))

        self._cursor_position = (col, row)  # (x, y)

    def scroll_display_left(self) -> None:
        """Scroll the display to the left by one"""
        self._command(value=(Const.LCD_CURSORSHIFT | Const.LCD_DISPLAYMOVE | Const.LCD_MOVELEFT))  # noqa: E501

    def scroll_display_right(self) -> None:
        """Scroll the display to the right by one"""
        self._command(value=(Const.LCD_CURSORSHIFT | Const.LCD_DISPLAYMOVE | Const.LCD_MOVERIGHT))  # noqa: E501

    def left_to_right(self) -> None:
        """Set text flow left to right"""
        self._display_mode |= Const.LCD_ENTRYLEFT
        self._command(value=(Const.LCD_ENTRYMODESET | self._display_mode))

    def right_to_left(self) -> None:
        """Set text flow right to left"""
        self._display_mode &= ~Const.LCD_ENTRYLEFT
        self._command(value=(Const.LCD_ENTRYMODESET | self._display_mode))

    def no_backlight(self) -> None:
        """Turn backlight off"""
        self._backlight_val = Const.LCD_NOBACKLIGHT
        self._expander_write(value=0)

    def backlight(self) -> None:
        """Turn backlight on"""
        self._backlight_val = Const.LCD_BACKLIGHT
        self._expander_write(value=0)

    def autoscroll(self) -> None:
        """Set text 'right justified' from the cursor"""
        self._display_mode |= Const.LCD_ENTRYSHIFTINCREMENT
        self._command(value=(Const.LCD_ENTRYMODESET | self._display_mode))

    def no_autoscroll(self) -> None:
        """Set text 'left justified' from the cursor"""
        self._display_mode &= ~Const.LCD_ENTRYSHIFTINCREMENT
        self._command(value=(Const.LCD_ENTRYMODESET | self._display_mode))

    def create_char(self, location: int, char_map: list[int]) -> None:
        """
        Fill the first 8 CGRAM locations with custom characters

        :param      location:  The location to store the custom character
        :param      char_map:   The char_map aka custom character
        """
        location &= 0x7  # we only have 8, locations 0-7

        self._command(value=(Const.LCD_SETCGRAMADDR | location << 3))
        sleep_us(40)

        for x in range(0, 8):
            self._command(value=char_map[x], mode=Const.RS)
            sleep_us(40)

    def print(self, text: str) -> None:
        """
        Print text on LCD
        """
        _cursor_x, _cursor_y = self.cursor_position

        for char in text:
            self._command(value=ord(char), mode=Const.RS)

        self.cursor_position = (_cursor_x + len(text), _cursor_y)

    def _command(self, value: int, mode: int = 0) -> None:
        """
        Send 8 bits command to I2C device

        :param      value:  The value
        """
        high_nib = value & 0xF0
        low_nib = (value << 4) & 0xF0
        self._write_4_bits(value=(high_nib | mode))
        self._write_4_bits(value=(low_nib | mode))

    def _write_4_bits(self, value: int) -> None:
        """
        Write 4 bits to I2C device

        :param      value:  The value to send
        """
        self._expander_write(value=value)
        self._pulse_enable(value=value)

    def _pulse_enable(self, value: int) -> None:
        """
        Pulse Enable (EN) pin

        :param      value:  The value to send
        """
        # Set Enable (EN) pin HIGH, pulse must be >450ns
        self._expander_write(value=(value | Const.EN))
        sleep_us(1)

        # Set Enable (EN) pin LOW, needs >37us to settle
        self._expander_write(value=(value & ~Const.EN))
        sleep_us(50)

    def _expander_write(self, value: int) -> None:
        """
        Write data to I2C device (port expander)

        :param      value:  The value to send
        """
        self._i2c.writeto(self.addr, bytes([value | self._backlight_val]))
