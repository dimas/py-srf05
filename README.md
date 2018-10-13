# py-srf05
A very simple Python interface to SFR05 ultrasonic module

```python
GPIO.setmode(GPIO.BCM)

sensor = SRF05(trigger_pin = 15, echo_pin = 14)
while True:
    print(sensor.measure())
```

prints didtance in centimeters.

# Notes

The SRF05 and Python combination are only good for really simple use cases, basically to experiment and play with.
The nature of SRF05 requires accurate measurement of time which just cannot work reliably if you go
beyond a simple example. The moment you start loading your CPU with other processes or start using threads
in your Python application, it will start affecting your measurements.

You need to be prepared to treat SRF05 readings as raw data, filter outliers and all that.

If you want reliable distance measurement that is not affected by other threads/processes - the simplest
solution is to get a distance sensor that times the echo response internally and gives you the distance
value via a digital interface like I2C.
