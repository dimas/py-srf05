import RPi.GPIO as GPIO
import SRF05

GPIO.setmode(GPIO.BCM)

sensor = SRF05.SRF05(trigger_pin = 15, echo_pin = 14)
while True:
    print(sensor.measure())
