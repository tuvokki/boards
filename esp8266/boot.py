import network
from utime import sleep, ticks_ms, ticks_diff


SSID = ""
PASSWORD = ""


def network_connect():
    print("Connecting to WiFi Network Name:", SSID)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Waiting for wifi chip to power up...")
    start = ticks_ms()  # start a millisecond counter
    # wlan.scan()  # Scan for available access points
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)  # Connect to an AP
        print("Waiting for connection...")
        counter = 0
        while not wlan.isconnected():
            sleep(1)
            print(counter, ".", sep="", end="", )
            counter += 1
    # Change name/password of ESP8266"s AP:
    # ap_if = network.WLAN(network.AP_IF)
    # ap_if.config(ssid=SSID, security=network.AUTH_WPA_WPA2_PSK, key=PASSWORD)
    delta = ticks_diff(ticks_ms(), start)
    print("Connect Time:", delta, "milliseconds")
    print("IP Address:", wlan.ifconfig()[0])


print("Boot finished. Starting network ... ")
network_connect()

