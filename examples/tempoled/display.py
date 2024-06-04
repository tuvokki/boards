import _thread
import time

from framebuf import FrameBuffer, MONO_HLSB

from gui.core.writer import Writer  # Renders text
from gui.core.nanogui import refresh
from gui.fonts import arial10, courier20, font6
from gui.widgets.label import Label
from color_setup import ssd


def init_display():
    """
    Initialise and clear display.
    """
    refresh(ssd, True)
    Writer.set_textpos(ssd, 0, 0)  # In case previous tests have altered it

    # Instantiate any Writers to be used (one for each font)
    # Monochrome display uses Writer
    wri = Writer(ssd, font6, verbose=False)
    # wri = Writer(ssd, arial10, verbose=False)
    # wri = Writer(ssd, courier20, verbose=False)
    wri.set_clip(True, True, False)
    return ssd, wri


class Bitmaps:
    """
    A bitmap is a bytearray and the size of the bitmap: `(bytearray([...]), x, y)`
    Usage: See Display.draw_symbol
    """
    sun = (bytearray([1, 0, 65, 4, 32, 8, 3, 128, 15, 224, 15, 224, 31, 240,
                      223, 246, 31, 240, 15, 224, 15, 224, 3, 128, 32, 8, 65, 4, 1, 0, 0, 0]),
           16, 16)
    thermometer = (bytearray([8, 20, 212, 20, 20, 220, 28, 28, 220, 28, 62, 127, 127, 127, 62, 28]),
                   8, 16)
    droplet = (bytearray([0, 4, 8, 8, 24, 24, 60, 60, 126, 126, 255, 255, 255, 255, 126, 60]),
               8, 16)
    cloud = (bytearray([3, 192, 7, 224, 15, 240, 127, 254, 255, 255, 255, 255, 255, 255, 127, 254]),
             16, 8)
    rain = (bytearray([33, 8, 66, 16, 132, 32]),
            16, 3)
    check_open = (bytearray([254,130,130,130,130,130,254,0]),
                  8, 8)
    check_close = (bytearray([254,198,170,146,170,198,254,0]),
                  8, 8)
    lightning = (bytearray([3, 224, 7, 192, 15, 128, 3, 192, 7, 0, 6, 0, 8, 0]),
                 16, 7)
    smiley = (bytearray([1, 128, 6, 96, 24, 24, 32, 4, 32, 4, 66, 66, 64, 2, 128, 1,
                         128, 1, 68, 34, 66, 66, 33, 132, 32, 4, 24, 24, 6, 96, 1, 128]),
              16, 16)
    _list = []

    def __init__(self):
        self._list = [b for b in dir(Bitmaps) if b[0] != "_"]


class Display:
    def __init__(self):
        self.display, self.wri = init_display()
        self._flash()
        self.active_label_anim = False

    def refresh(self):
        # refresh(self.display)
        self.display.show()

    def _flash(self, times: int = 1, duration: float = 0.2):
        for _ in range(times):
            self.display.fill(1)
            self.refresh()
            time.sleep(duration)
            self.display.fill(0)
            self.refresh()

    def _active_label(self, text: str = "Booting", clear: bool = True):
        label = Label(self.wri, 0, 0, text)
        msg = f"{text} "
        while self.active_label_anim:
            if msg[-3:] == "...":
                label.value(f"{text}    ")
                self.refresh()
                msg = f"{text} "
            else:
                msg = f"{msg}."
            label.value(msg)
            self.refresh()
            time.sleep(0.1)
        if clear:
            print("Clear label")
            # overwrite with 32 whitespaces
            label.value("                                ")
            self.refresh()

    def clear(self):
        self.display.fill(0)
        self.refresh()

    def show_boot_message(self, duration: float = 3.0):
        print("Start boot message")
        self.active_label_anim = True
        _thread.start_new_thread(self._active_label, ("Booting",))
        time.sleep(duration)
        self.active_label_anim = False
        print("Boot message finished")

    def top_left_count(self, total: int = 16, back: bool = True, clear: bool = True):
        label = Label(self.wri, 0, 104, self.wri.stringlen('10'))
        if back:
            count_rng = range(total, -1, -1)
        else:
            count_rng = range(total)
        for i in count_rng:
            label.value(f"{i:>2}")
            self.refresh()
            time.sleep(0.1)
        if clear:
            # TODO: How to properly clear a label?
            label.value("  ")

    def draw_symbol(self, bitmap: str, pos_x: int = 0, pos_y: int = 0, ):
        if bitmap not in Bitmaps()._list:
            print(f"No such bitmap. Possible options: {Bitmaps()._list}.")
            return

        b_arr, width, height = getattr(Bitmaps, bitmap)
        fb = FrameBuffer(b_arr, width, height, MONO_HLSB)
        self.display.blit(fb, pos_x, pos_y)
        self.refresh()

    def draw_borders(self, thick: bool = True):
        if thick:
            self.display.rect(0, 0, self.display.width, self.display.height, 1)
            self.display.rect(1, 1, self.display.width - 2, self.display.height - 2, 1)
        else:
            self.display.rect(0, 0, self.display.width, self.display.height, 1)
        self.refresh()

    def _clear_title(self, write: bool = True):
        for y in range(3, 10):
            for x in range(3, 125):
                self.display.pixel(x, y, 0)
        if write:
            self.refresh()

    def write_title(self, text: str = None):
        self._clear_title(False)
        if text:
            self.display.text(text, 3, 3)
        self.refresh()

    def show_welcome(self):
        self.draw_borders()
        self.write_title("Welcome")
        self.display.hline(0, 11, 128, 1)
        self.refresh()


def bitmap_show(d):
    for b in Bitmaps()._list:
        d.draw_symbol(b)
        Label(d.wri, 16, 0, b)
        d.refresh()
        time.sleep(1)
        d.display.fill(0)
    d.refresh()

def check_flash(d, times: int = 1, duration: float = 0.2):
    for _ in range(times):
        d.draw_symbol("check_open")
        time.sleep(duration/2)
        d.draw_symbol("check_close")
        time.sleep(duration/2)
