
servo = PWM(Pin(27), freq=5000, duty_u16=32768)
# get current frequency
freq = servo.freq()
print(f"freq: {freq}")
# set PWM frequency from 1Hz to 40MHz
# servo.freq(1000)

# get current duty cycle, range 0-1023 (default 512, 50%)
duty = servo.duty_u16()
print(f"duty: {duty}")
# set duty cycle from 0 to 1023 as a ratio duty/1023, (now 25%)
servo.duty_u16(0)
print(f"duty: {duty}")
servo.duty_u16(256)
print(f"duty: {duty}")
servo.duty_u16(512)
print(f"duty: {duty}")
servo.duty_u16(1023)
print(f"duty: {duty}")
#
# get current duty cycle, range 0-65535
# duty_u16 = servo.duty_u16()
# set duty cycle from 0 to 65535 as a ratio duty_u16/65535, (now 75%)
# servo.duty_u16(2**16*3//4)
#
# get current pulse width in ns
# duty_ns = servo.duty_ns()
# set pulse width in nanoseconds from 0 to 1_000_000_000/freq, (now 25%)
# servo.duty_ns(250_000)

# turn off PWM on the pin
servo.deinit()

# create and configure in one go
# pwm2 = PWM(Pin(2), freq=20000, duty_u16=512)
# view PWM settings
# print(pwm2)
