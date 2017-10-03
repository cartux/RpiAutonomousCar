import time

import RPi.GPIO as GPIO


# TODO: This should be a context manager too. We might think about
# subclassing these all into a common class that keeps track of its instances
# and cleans up when the last of them is destroyed. See
# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
# The reason for this is that it's a bit dangerous to be using GPIO.cleanup()
# when other pins are in use because this clears all the pins. For this
# reason, this would normally be called at the very end of a script. So we
# don't have to solve this right at this moment, but if we have a lot of time
# after refactoring we might think about how to cleanup the GPIOs the best way.
class LED():

    # TODO: Add docstring

    def __init__(self):
        # TODO: Move this attribute into class, it's always the same
        self._LedPin = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._LedPin, GPIO.OUT)

    # TODO: PEP8
    def ledOn(self):
        GPIO.output(self._LedPin,1)

    def ledOff(self):
        GPIO.output(self._LedPin,0)

    # TODO: This goes into __exit__
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

