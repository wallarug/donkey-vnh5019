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
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.PWM as PWM

# Motor Driver Sheild GPIO Numbers
VNH_SHIELD_M1INA = 5
VNH_SHIELD_M1INB = 4        
VNH_SHIELD_M1EN = 6
VNH_SHIELD_M2INA = 17
VNH_SHIELD_M2INB = 18
VNH_SHIELD_M2EN = 22
VNH_SHIELD_M1PWM = 19
VNH_SHIELD_M2PWM = 20


class VNH5019(object):
    """ Polulu VNH5019 Motor Controller. """

    def __init__(self, ina, inb, enable, ctrl,
                 enable_pwm=enable_pwm
                 gpio=GPIO.get_platform_gpio()
                 pwm=PWM.get_platform_pwm() ):
        # Save GPIO state and pin numbers
        self._en = enable
        self._ina = ina
        self._inb = inb
        self._ctrl = ctrl

        # Save libraries
        self._enable_pwm = enable_pwm
        self._pwm = pwm
        self._gpio = gpio

        # Setup all pins as outputs
        for pin in (ina, inb, enable):
            gpio.setup(pin, GPIO.OUT)

        # Setup the PWM speed control
        if enable_pwm:
            pwm.start(ctrl, 0)
        else:
            gpio.setup(ctrl, GPIO.OUT)
            self._gpio.output(ctrl, False)

        # Initialise the motor (stationary)
        self.setBreak()

    ## Stop the motor from spinning
    def setBreak(self):
        # set both in channels to low
        self._gpio.output(self._ina, False)
        self._gpio.output(self._inb, False)

    ## Set speed for motor, speed is a number between -400 and 400
    def setSpeed(self, speed):
        reverse = False
        
        if ( speed < 0 ):
            speed = -speed  # Make speed a positive quantity
            reverse = True  # Preserve the direction

        if ( speed > 400 ):
            speed = 400     # Max PWM duty cycle

        # Set the speed of the motor
        if (self._enable_pwm):
            self._pwm.set_duty_cycle(self._ctrl, speed / 4)
        else:
            self._gpio.output(self._ctrl, True)

        # Determine direction to spin motors
        if ( speed == 0 ):
            self._gpio.output(self._ina, False) # make the motor coast no 
            self._gpio.output(self._inb, False) # matter which direction it is spinning.
        elif ( reverse ):
            self._gpio.output(self._ina, False)
            self._gpio.output(self._inb, True)
        else:
            self._gpio.output(self._ina, True)
            self._gpio.output(self._inb, False)
        
        

class DualVNH5019MotorShield(object):
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
