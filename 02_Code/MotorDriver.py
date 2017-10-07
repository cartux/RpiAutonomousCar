#!/usr/bin/python
import sys
import time

import RPi.GPIO as GPIO


# TODO: DRY this code (WET)
# TODO: This class cleans up after itself, so it should be used as a context
# manager like this:
# with MotorDriver() as m:
#     m.do_stuff()
# ...
# When an exception occurs or the with-block is completed, the object cleans
# up after itself automatically.
class MotorDriver():

    """Class to represent TB6612FNG DC Motor driver."""
    # TODO: Define method __enter__ which returns self for use in with clause
    # TODO: Class attributes go here

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        # Initialise inputs & outputs pins
        # TODO: These are shared across all objects, so make them class
        # attributes rather than setting them on initialization
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

    # TODO: Each direction sets 4 GPIOs, we can store these in the class, e.g.
    # >>> md = MotorDriver()
    # >>> md.drive(md.directions.left)
    # And then this would call internally something like:
    # (inside MotorDriver):
    # ...
    #     def drive(direction, duty_cycle):
    #         for pin, val in direction:
    #             GPIO.output(pin, val)
    # Here the directions would be on the class, stored as a tuple of tuples,
    #  where each inner tuple would store the pin and the value it should be
    # set to.

    # TODO: argument PEP8
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

    # TODO: Rename to __exit__ so that this is called on exceptions or when
    # exiting context
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
