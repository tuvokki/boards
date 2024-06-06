import time
import ubluetooth
from machine import Pin


class BLE:
    def __init__(self, name, debug: bool = False):
        self.beep_time = 0.5
        self.name = name
        self.debug = debug
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

        self.led = Pin(2, Pin.OUT)
        self.horn = Pin(19, Pin.OUT)

        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):
        self.led(1)

    def disconnected(self):
        self.led(0)

    def ble_irq(self, event, data):
        if self.debug:
            print(f"Received BLE irq event: [{event}]\n\twith data: {data}")

        if event == 1:
            """Central disconnected"""
            self.connected()

        elif event == 2:
            """Central disconnected"""
            self.advertiser()
            self.disconnected()

        elif event == 3:
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode("UTF-8").strip()
            if message == "toggle_led":
                if self.debug:
                    print(f"toggle_led: {self.led}")
                self.led.value(not self.led.value())
                self.send(f"Led {self.led} is now {self.led.value()}")
            elif message == "blink_led":
                if self.debug:
                    print(f"blink_led {self.led}")
                for _ in range(10):
                    self.led.value(not self.led.value())
                    time.sleep(0.2)
            elif message == "beep":
                if self.debug:
                    print(f"beep for {self.beep_time}")
                self.horn.on()
                time.sleep(self.beep_time)
                self.horn.off()
            else:
                print(f"fReceived unknown event:\n\tmessage: {message}")

    def register(self):
        # Nordic UART Service (NUS)
        NUS_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
        RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
        TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)

        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART,)
        ((self.tx, self.rx,),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + "\n")

    def advertiser(self):
        name = bytes(self.name, "UTF-8")
        self.ble.gap_advertise(100, bytearray("\x02\x01\x02", "utf8") + bytearray((len(name) + 1, 0x09), "utf8") + name)


print("Finished main")
ble = BLE("Hello32")

"""
# Copy code for repl
from main import BLE

ble = BLE("Hello32")
ble.send("Hello World")
"""
