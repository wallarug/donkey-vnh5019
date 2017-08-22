#!/bin/python3

#
# Author: Cian Byrne (wallarug)
#
#
# ## Pin Mappings ##
# | Arduino | VNH5019 | BCM GPIO |
# |---------|---------|----------|
# |  D2     | M1 INA  |     5    |
# |  D4     | M1 INB  |     4    |
# |  D6     | M1 EN   |     6    |
# |  D7     | M2 INA  |     17   |
# |  D8     | M2 INB  |     18   |
# |  D9     | M1 PWM  |     19   |
# |  D10    | M2 PWM  |     20   |
# |  D12    | M2 EN   |     22   |
# |  A0     | M1 CS   |     nc   |
# |  A1     | M2 CS   |     nc   |
#


import time

        


class VNH5019(object):
    """ Polulu VNH5019 Motor Controller. """

    def __init__(self, controller, num):
        self.MC = controller
        self.motornum = num
        pwm = en = in1 = in2 = 0

        if (num == 0):
            pwm = 19
            in2 = 4
            in1 = 5
            en = 16
        elif (num == 1):
            pwm = 20
            in2 = 18
            in1 = 17
            en = 22
        else:
            raise NameError('Pololu Motor must be between 1 and 2')

        self.PWMpin = pwm
        self.IN1pin = in1
        self.IN2pin = in2
        self.ENpin = en
        
        

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

    def run(self, command):
        if not self.MC:
            return
        if (command == DualVNH5019MotorShield.FORWARD):
            self.MC.setPin(self.IN2pin, 0)
            self.MC.setPin(self.IN1pin, 1)
            self.MC.setPin(self.ENpin, 1)
        if (command == DualVNH5019MotorShield.BACKWARD):
            self.MC.setPin(self.IN1pin, 0)
            self.MC.setPin(self.IN2pin, 1)
            self.MC.setPin(self.ENpin, 1)
        if (command == DualVNH5019MotorShield.RELEASE):
            self.MC.setPin(self.IN1pin, 0)
            self.MC.setPin(self.IN2pin, 0)
            self.MC.setPin(self.ENpin, 1)

    def setSpeed(self, speed):
        if (speed < 0):
            speed = 0
        if (speed > 255):
            speed = 255
        self.MC._pwm.setPWM(self.PWMpin, 0, speed*16)
        

class DualVNH5019MotorShield:
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3
    RELEASE = 4

    SINGLE = 1
    DOUBLE = 2

    def __init__(self):
        self.motors = [ VNH5019(self, m) for m in range(2) ]

        # GPIO setup for Raspberry Pi
        for motor in self.motors:
            GPIO.setup(motor.IN1pin, GPIO.OUT)
            GPIO.setup(motor.IN2pin, GPIO.OUT)
            GPIO.setup(motor.ENpin, GPIO.OUT)
            GPIO.setup(motor.PWMpin, GPIO.OUT)

    def setPin(self, pin, value):
        if (pin < 0) or (pin > 22):
            raise NameError('Pin must be between 0 and 22 inclusive')
        if (value != 0) and (value != 1):
            raise NameError('Pin value must be 0 or 1!')

        GPIO.output(pin, value)

    def setPWM(self, pin, value):
        GPIO.
