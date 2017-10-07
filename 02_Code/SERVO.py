import time
import RPi.GPIO as GPIO


# TODO: Is this used anywhere? Otherwise let's remove it.
# TODO: Rename, all caps looks like constant & immutable. Plus docstrings.
class SERVO():
    def __init__(self):
        # TODO: PEP8, plus make this class attribute.
        self._ServoPin = 4
        # TODO: Long-term we should think about if we set the GPIO mode in
        # each hardware class - it's a lot of setting on initialization and
        # would probably be more efficient to have some kind of managing
        # class that takes care of all these things for us and gives us the
        # sensors, servos, etc. via a factory. Not important now though.
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._ServoPin, GPIO.OUT)
        # TODO: PEP8
        self._ServoPWM = GPIO.PWM(self._ServoPin,50)
        self._ServoPWM.start(7.5)


    def loop(self):
        while True:
            self._ServoPWM.ChangeDutyCycle(7.5)
            time.sleep(1)
            self._ServoPWM.ChangeDutyCycle(12.5)
            time.sleep(1)
            self._ServoPWM.ChangeDutyCycle(2.5)
            time.sleep(1)

    def destroy(self):
        self._ServoPWM.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    servo = SERVO()
    try:
        servo.loop()
    except KeyboardInterrupt:
        servo.destroy()

