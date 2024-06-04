import _thread

import network
from utime import sleep, ticks_ms, ticks_diff

from libs import MicroPyServer
from credentials import Credentials


def network_connect():
    print('Connecting to WiFi Network Name:', Credentials.SSID)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print('Waiting for wifi chip to power up...')
    start = ticks_ms()  # start a millisecond counter
    # wlan.scan()  # Scan for available access points
    if not wlan.isconnected():
        wlan.connect(Credentials.SSID, Credentials.PASSWORD)  # Connect to an AP
        print("Waiting for connection...")
        counter = 0
        while not wlan.isconnected():
            sleep(1)
            print(counter, '.', sep='', end='', )
            counter += 1

    delta = ticks_diff(ticks_ms(), start)
    print("Connect Time:", delta, 'milliseconds')
    print('IP Address:', wlan.ifconfig()[0])
    return wlan


def index(_request):
    html = """<!DOCTYPE html>
    <html>
       <head>
         <title>Web Server On ESP32 </title>
         <link rel="stylesheet" href="https://unpkg.com/chota@latest">
       </head>
      <body>
          <h1>ESP32 Wireless Web Server</h1>
      </body>
    </html>
    """
    server.send(html)


server = MicroPyServer()
''' add route '''
server.add_route("/", index)
''' start server '''


def start():
    server_thread = None
    netw = network_connect()
    if netw.isconnected:
        server_thread = _thread.start_new_thread(server.start, ())
    return server_thread
