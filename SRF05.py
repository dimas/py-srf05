import RPi.GPIO as GPIO
import time

# A very simple Python interface to SFR05 module (probably will work with SFR04 too but I have no tried).
# Just call measure() method and it will return you distance in centimeters or None.
#
# IMPORTANT NOTE: in order to read data from the sensor we need to measure width of an echo pulse
# and we need to be accurate enough. This obviously is not going to work well if your CPU is heavily loaded.
# Plus, Python with its GIL is just not the best environment for these things if you have other threads running.
# But make no mistake - doing that in C is not a silver bullet either even if done properly with interrupts etc.
# Sure, C version would have better accuracy but if you really want to avoid interference with other threads/processes,
# you should use a sensor that times echo iself and then gives you result via digital interface (like I2C or SPI).
#
# The document I am referring throught the code is https://www.robot-electronics.co.uk/htm/srf05tech.htm
#
class SRF05:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        self.trigger_time = 0

        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.setup(self.trigger_pin, GPIO.OUT)

    def measure(self):
        now = self.time_us()

        # "The SRF05 can be triggered as fast as every 50mS, or 20 times each second.
        # You should wait 50ms before the next trigger, even if the SRF05 detects a close object and the echo pulse is shorter.
        # This is to ensure the ultrasonic "beep" has faded away and will not cause a false echo on the next ranging."
        pause = 50000 - (now - self.trigger_time)
        if pause > 0:
            self.sleep_us(pause)

        self.trigger()

        self.trigger_time = self.time_us()

        # "The SRF05 will send out an 8 cycle burst of ultrasound at 40khz and raise its echo line high (or trigger line in mode 2)"
        # Wait no longer than 30ms
        if GPIO.wait_for_edge(self.echo_pin, GPIO.RISING, timeout=30) is None:
            return None

        start = self.time_us()

        # Measure pulse duration, again do not wait more than 30ms
        # "If nothing is detected then the SRF05 will lower its echo line anyway after about 30mS."
        if GPIO.wait_for_edge(self.echo_pin, GPIO.FALLING, timeout=30) is None:
            return None

        end = self.time_us()

        width = end - start

        # ...and by that logic we should not have real measurement with pulse longer than 30ms anyway
        if width > 30000:
            return None

        # "If the width of the pulse is measured in uS, then dividing by 58 will give you the distance in cm,
        # or dividing by 148 will give the distance in inches. uS/58=cm or uS/148=inches."
        return int(width / 58)

    def trigger(self):
        # "You only need to supply a short 10uS pulse to the trigger input to start the ranging."
        GPIO.output(self.trigger_pin, 1)
        self.sleep_us(10)
        GPIO.output(self.trigger_pin, 0)

    # Return time in microseconds
    def time_us(self):
        return int(time.time() * 1000000)

    def sleep_us(self, us):
        time.sleep(us / 1000000.0)
