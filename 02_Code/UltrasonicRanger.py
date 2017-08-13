#!/usr/bin/env python
import time

import RPi.GPIO as GPIO


# TODO: We need docstrings for each method
class SensingTimeoutError(Exception):

    """Sensor needed too long for response."""


class UltrasonicRanger():

    """Interface with an HCSR04 ultrasonic range sensor."""

    def __init__(self):
        self._trigger_pin = 15
        self._echo_pin = 14
        self._timeout  = 0.10 #[s]
        self._average_count = 10

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._trigger_pin, GPIO.OUT)
        GPIO.setup(self._echo_pin, GPIO.IN)

    # TODO: Change to property. Does this do anything?
    def get_distance(self):
        #send impulse
        GPIO.output(self._trigger_pin, 0)
        time.sleep(0.000002)

        GPIO.output(self._trigger_pin, 1)
        time.sleep(0.00001)
        GPIO.output(self._trigger_pin, 0)

        #timeout
        timeout_end = time.time()+ self._timeout

        # TODO: Explicit exception, e.g. SensingTimeoutError
        #wait for response
        while GPIO.input(self._echo_pin) == 0:
            if time.time() > timeout_end:
                return -1, -1
        time1 = time.time()
        while GPIO.input(self._echo_pin) == 1:
            if time.time() > timeout_end:
                return -1, -1
        time2 = time.time()

        #calculate the distance
        during = time2 - time1
        return 1, during * 340.0 / 2.0 * 100

    # TODO: Eliminate multiple return statements
    def get_average_distance(self):
        """Return measured distance in cm."""
        i = 0
        distance = 0
        errorCount = 0
        while i < self._average_count:
            qualifier, tmp = self.get_distance()
            if qualifier != -1:
                i = i + 1
                distance = distance + tmp
            else:
                errorCount = errorCount
            # TODO: Simplify. This should be replaced with an exception, e.g.
            # raise BadDistanceException()
            if errorCount > 3:
                return -1, -1
        return 1, distance/(self._average_count * 1.0)


    # TODO: Replace this with a context handler
    # with UltrasonicSensor() as u_s:
    #     do_something()
    # # Then the sensor would destroy itself when it closes
    def destroy(self):
        GPIO.cleanup()


if __name__ == "__main__":
    ultrasonic = UltrasonicRanger()
    try:
        while True:
            qualifier,dis = ultrasonic.get_average_distance()
            if qualifier == 1:
                # TODO: Use new-style print syntax (print("Hello world!"))
                print dis, 'cm'
            else:
                print "Error duringn reading"

            time.sleep(1)

    except KeyboardInterrupt:
        ultrasonic.destroy()
