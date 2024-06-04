from libs import RGBLed
from temperature_sensor import TemperatureSensor
from utils import *

flash()

myRGB = RGBLed(23, 22, 21)

temperature_sensor = TemperatureSensor(sensor_pin=4)
temperature_sensor.continuous_temp_read = False

