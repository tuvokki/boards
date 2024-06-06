esptool.py --chip esp32 --port /dev/cu.usbserial-0001 erase_flash
esptool.py --chip esp32 --port /dev/cu.usbserial-0001 --baud 460800 write_flash -z 0x1000 archives/micropython/ESP32_GENERIC-20240222-v1.22.2.bin

