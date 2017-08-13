import time

import RPi.GPIO as GPIO


class LED():
    def __init__(self):
        self._LedPin = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._LedPin, GPIO.OUT)

    def ledOn(self):
        GPIO.output(self._LedPin,1)

    def ledOff(self):
        GPIO.output(self._LedPin,0)

    def destroy(self):
        GPIO.cleanup()

if __name__ == "__main__":

    led = LED()
    try:
        while 1:
            led.ledOn()
            time.sleep(0.5)
            led.ledOff()
            time.sleep(0.5)

    except KeyboardInterrupt:
        led.destroy()


