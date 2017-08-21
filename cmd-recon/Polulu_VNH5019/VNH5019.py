#!/bin/python3

#
# Author: Cian Byrne (wallarug)
#
#
#
#
#
#
#
#


import time


class VNH5019(object):
    """ Polulu VNH5019 Motor Controller. """

    def __init__(self, EN, INA, INB, PWM):
        import RPi.GPIO as GPIO
        self._pinA = INA
        self._pinB = INB
        self._pinEn = EN
        self._pinPWM = PWM
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pinEn, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pinA, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self._pinB, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PWM, GPIO.OUT)

        self._pinPWM = GPIO.PWM(PWM, 50)

    def shutdown(self):

        import RPi.GPIO as GPIO
        GPIO.cleanup()
