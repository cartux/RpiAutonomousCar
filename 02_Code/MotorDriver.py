#!/usr/bin/python
import sys
import time

import RPi.GPIO as GPIO


class MotorDriver():

    """Class to represent TB6612FNG DC Motor driver."""

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        # Initialise inputs & outputs pins
        self._M1Dir1Pin = 6
        self._M1Dir2Pin = 12
        self._M1PWMPin = 5
        self._M2Dir1Pin = 19
        self._M2Dir2Pin = 16
        self._M2PWMPin = 26
        self._STBYPin = 13

        # Set all the drive pins as output pins
        GPIO.setup(self._M1Dir1Pin, GPIO.OUT)
        GPIO.setup(self._M1Dir2Pin, GPIO.OUT)
        GPIO.setup(self._M1PWMPin, GPIO.OUT)
        GPIO.setup(self._M2Dir1Pin, GPIO.OUT)
        GPIO.setup(self._M2Dir2Pin, GPIO.OUT)
        GPIO.setup(self._M2PWMPin, GPIO.OUT)
        GPIO.setup(self._STBYPin, GPIO.OUT)

        # Initialise and start SW pwm engine
        self._M1Pwm = GPIO.PWM(self._M1PWMPin, 10000)
        self._M1Pwm.start(0)
        self._M2Pwm = GPIO.PWM(self._M2PWMPin, 10000)
        self._M2Pwm.start(0)

    def forward(self, dutyCycle=20):
        GPIO.output(self._M1Dir1Pin, 0)
        GPIO.output(self._M1Dir2Pin, 1)
        self._M1Pwm.ChangeDutyCycle(dutyCycle)

        GPIO.output(self._M2Dir1Pin, 1)
        GPIO.output(self._M2Dir2Pin, 0)
        self._M2Pwm.ChangeDutyCycle(dutyCycle)

        GPIO.output(self._STBYPin, 1)

    def reverse(self, dutyCycle=20):
        GPIO.output(self._M1Dir1Pin, 1)
        GPIO.output(self._M1Dir2Pin, 0)
        self._M1Pwm.ChangeDutyCycle(dutyCycle)

        GPIO.output(self._M2Dir1Pin, 0)
        GPIO.output(self._M2Dir2Pin, 1)
        self._M2Pwm.ChangeDutyCycle(dutyCycle)

        GPIO.output(self._STBYPin, 1)

    def left(self, dutyCycle=8):
        GPIO.output(self._M1Dir1Pin, 1)
        GPIO.output(self._M1Dir2Pin, 0)
        self._M1Pwm.ChangeDutyCycle(dutyCycle)

        GPIO.output(self._M2Dir1Pin, 1)
        GPIO.output(self._M2Dir2Pin, 0)
        self._M2Pwm.ChangeDutyCycle(dutyCycle)

        GPIO.output(self._STBYPin, 1)

    def right(self, dutyCycle=8):
        GPIO.output(self._M1Dir1Pin, 0)
        GPIO.output(self._M1Dir2Pin, 1)
        self._M1Pwm.ChangeDutyCycle(dutyCycle)

        GPIO.output(self._M2Dir1Pin, 0)
        GPIO.output(self._M2Dir2Pin, 1)
        self._M2Pwm.ChangeDutyCycle(dutyCycle)

        GPIO.output(self._STBYPin, 1)

    def stop(self):
        GPIO.output(self._M1Dir1Pin, 0)
        GPIO.output(self._M1Dir2Pin, 0)
        # self._M1Pwm.stop()
        self._M1Pwm.ChangeDutyCycle(0)

        GPIO.output(self._M2Dir1Pin, 0)
        GPIO.output(self._M2Dir2Pin, 0)
        # self._M2Pwm.stop()
        self._M2Pwm.ChangeDutyCycle(0)

        GPIO.output(self._STBYPin, 0)

    def destroy(self):
        self._M1Pwm.stop()
        self._M2Pwm.stop()
        GPIO.cleanup()


if __name__ == '__main__':
    tb6612fng = MotorDriver()
    try:
        while True:
            tb6612fng.forward(10)
            time.sleep(1)

            tb6612fng.stop()
            time.sleep(1)

            tb6612fng.reverse(10)
            time.sleep(1)

            tb6612fng.stop()
            time.sleep(1)

            tb6612fng.left(5)
            time.sleep(1)

            tb6612fng.stop()
            time.sleep(1)

            tb6612fng.right(5)
            time.sleep(1)

            tb6612fng.stop()
            time.sleep(1)
            print("done")



    except KeyboardInterrupt:
        tb6612fng.destroy()
        sys.exit(0)
