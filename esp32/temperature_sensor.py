import _thread
import time

from libs import DS18X20


class TemperatureSensor:
    sensor = None
    continuous_temp_read = True
    debug = False
    last_readout = None

    def __init__(self, sensor_pin: int = 4):
        self.ds_sensor: DS18X20 = DS18X20(sensor_pin)
        roms = self.ds_sensor.scan()
        if len(roms) > 1:
            raise Exception("This class cannot handle more than one sensor on pin {}".format(sensor_pin))

        self.sensor: bytearray = roms[0]
        if self.debug:
            print('Initialized sensor device: ', self.sensor)

    def read(self):
        self.ds_sensor.convert_temp()
        time.sleep(0.75)
        self.last_readout = self.ds_sensor.read_temp(self.sensor)
        return self.last_readout

    def read_temperature(self, interval: float = 2.0, duration: float = None):
        if duration:
            start = time.ticks_ms()
        while True:
            print(self.read())
            time.sleep(interval)
            if duration and time.ticks_diff(time.ticks_ms(), start) >= duration * 1000:
                if self.debug:
                    print(f"Elapsed time is {time.ticks_diff(time.ticks_ms(), start) / 1000}, stopping")
                break
            if not self.continuous_temp_read:
                if self.debug:
                    print(f"Value continuous_temp_read is set to {self.continuous_temp_read}, stopping")
                break

    def start_read(self):
        _thread.start_new_thread(self.read_temperature, (0.5, 10))

    def __str__(self):
        return f"TemperatureSensor on pin {self.ds_sensor.ow.pin}."

    def __repr__(self):
        repr_str = f"{self}\n"
        repr_str += f"\tsensor: {self.sensor}\n"
        repr_str += f"\tds_sensor: {self.ds_sensor}\n"
        repr_str += f"\tcontinuous_temp_read: {self.continuous_temp_read}\n"
        repr_str += f"\tlast readout: {self.last_readout}"
        if self.debug:
            repr_str += f"\n\tdebug: {self.debug}"

        return repr_str
