#!/usr/bin/env python

import time

from LED import LED
from MotorDriver import MotorDriver
from UltrasonicRanger import UltrasonicRanger


def loop(sensor, drive):
    duty_cycle = 4

    while True:
        # TODO: Replace with try-except clause, e.g.
        # try:
        #      distance = sensor.get_average_distance()
        # except BadDistanceException:
        #      pass
        qualifier, distance = sensor.get_average_distance()
        if qualifier == 1:
            if distance < 20:
                drive.stop()
                time.sleep(0.01)
                drive.reverse(duty_cycle - 2)
                time.sleep(0.25)
                drive.left(duty_cycle - 2)
                time.sleep(0.25)
                drive.forward(duty_cycle)
            else:
                drive.forward()

        else:
            pass


if __name__ == "__main__":
    try:
        ultrasonic = UltrasonicRanger()
        led = LED()
        robot_drive = MotorDriver()
        loop(ultrasonic, robot_drive, led)
    except KeyboardInterrupt:
        ultrasonic.destroy()
