import logging

import ubluetooth
from machine import Pin

logger = logging.getLogger(__name__)


class BLE():
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

        self.led = Pin(2, Pin.OUT)

        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):
        self.send("Welcome to ESP32")

    def disconnected(self):
        ...

    def ble_irq(self, event, data):
        if event == 1:
            '''Central disconnected'''
            self.connected()
            self.led(1)

        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()
            self.led(0)

        elif event == 3:
            # '''New message received'''            
            # self.led.value(not self.led.value())
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            logger.info(message)
            if message == 'red_led':
                self.led.value(not self.led.value())
                logger.info('red_led', self.led.value())
                self.send('red_led' + str(self.led.value()))
            else:
                self.send(message + " ==> " + str(self.led.value()))

    def register(self):
        # Nordic UART Service (NUS)
        NUS_UUID = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        RX_UUID = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        TX_UUID = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)

        BLE_UART = (BLE_NUS, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART,)
        ((self.tx, self.rx,),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray('\x02\x01\x02', 'utf8') + bytearray((len(name) + 1, 0x09), 'utf8') + name)


logger.info("Finished main")
'''
# Copy code for repl
from main import BLE

ble = BLE("ESP32")
ble.send("Hello World")
'''