#!/usr/bin/env python
import time

import RPi.GPIO as GPIO


class UltrasonicRanger():

    """Interface with an HCSR04 ultrasonic range sensor."""

    def __init__(self):
        self._TRIGPin = 15
        self._ECHOPin = 14
        self._timeout  = 0.10 #[s]
        self._averageCount = 10

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._TRIGPin, GPIO.OUT)
        GPIO.setup(self._ECHOPin, GPIO.IN)

    def get_distance(self):
        #send impulse
        GPIO.output(self._TRIGPin, 0)
        time.sleep(0.000002)

        GPIO.output(self._TRIGPin, 1)
        time.sleep(0.00001)
        GPIO.output(self._TRIGPin, 0)

        #timeout
        timeout_end = time.time()+ self._timeout

        #wait for response
        while GPIO.input(self._ECHOPin) == 0:
            if time.time() > timeout_end:
                return -1, -1
        time1 = time.time()
        while GPIO.input(self._ECHOPin) == 1:
            if time.time() > timeout_end:
                return -1, -1
        time2 = time.time()

        #calculate the distance
        during = time2 - time1
        return 1, during * 340.0 / 2.0 * 100

    def get_average_distance(self):
        i = 0
        distance = 0
        errorCount = 0
        while i < self._averageCount:
            qualifier, tmp = self.get_distance()
            if qualifier != -1:
                i = i + 1
                distance = distance + tmp
            else:
                errorCount = errorCount
            if errorCount > 3:
                return -1, -1
        return 1, distance/(self._averageCount*1.0)

    def destroy(self):
        GPIO.cleanup()


if __name__ == "__main__":
    ultrasonic = UltrasonicRanger()
    try:
        while True:
            qualifier,dis = ultrasonic.get_average_distance()
            if qualifier == 1:
                print dis, 'cm'
            else:
                print "Error duringn reading"

            time.sleep(1)

    except KeyboardInterrupt:
        ultrasonic.destroy()
