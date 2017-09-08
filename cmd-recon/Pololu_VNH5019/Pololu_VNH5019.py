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
VNH_SHIELD_M1INA = 17
VNH_SHIELD_M1INB = 27        
VNH_SHIELD_M1EN = 23
VNH_SHIELD_M2INA = 5
VNH_SHIELD_M2INB = 6
VNH_SHIELD_M2EN = 24
VNH_SHIELD_M1PWM = 22
VNH_SHIELD_M2PWM = 13


class Pololu_VNH5019(object):
    """ Class to represent and interact with a VNH5019 Motor Controller. """

    def __init__(self, ina, inb, enable, ctrl,
                 enable_pwm=True,
                 gpio=GPIO.get_platform_gpio(),
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
            self._gpio.setup(pin, GPIO.OUT)

        # Setup the PWM speed control
        if ( enable_pwm ):
            self._pwm.start(ctrl, 0)
        else:
            gpio.setup(ctrl, GPIO.OUT)
            self._gpio.output(ctrl, False)

        # Enable Motor
        self._gpio.output(self._en, True)

        # Initialise the motor (stationary)
        self.setBrake(0)

    ## Stop the motor from spinning
    def setBrake(self, brake):
        # brake is a number between 0 and 400
        # normalize brake
        if ( brake < 0 ):
            brake = -brake

        if ( brake > 400 ):     # Max brake
            brake = 400
        
        # set both in channels to low
        self._gpio.output(self._ina, False)
        self._gpio.output(self._inb, False)

        if ( self._enable_pwm ):
            self._pwm.set_duty_cycle(self._ctrl, brake / 4)
        else:
            self._gpio.output(self._ctrl, False)
            

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
        
        

class Pololu_DualVNH5019Shield(object):
    """ Class to represent and interact with a Pololu Dual VNH5019
         Motor Driver Shield with a Raspberry Pi """
    
    FORWARD = 1
    BACKWARD = 2
    BRAKE = 3
    RELEASE = 4

    def __init__(self,
                 m1ina=VNH_SHIELD_M1INA,
                 m1inb=VNH_SHIELD_M1INB,
                 m1en=VNH_SHIELD_M1EN,
                 m1pwm=VNH_SHIELD_M1PWM,
                 m2ina=VNH_SHIELD_M2INA,
                 m2inb=VNH_SHIELD_M2INB,
                 m2en=VNH_SHIELD_M2EN,
                 m2pwm=VNH_SHIELD_M2PWM,
                 pwm_enabled=True,
                 gpio=GPIO.get_platform_gpio(),
                 pwm=PWM.get_platform_pwm()):
        # Initialise Motors
        # Left Motor
        self._M1 = Pololu_VNH5019(m1ina,
                           m1inb,
                           m1en,
                           m1pwm,
                           enable_pwm=pwm_enabled,
                           gpio=gpio,
                           pwm=pwm)
        # Right Motor
        self._M2 = Pololu_VNH5019(m2ina,
                           m2inb,
                           m2en,
                           m2pwm,
                           enable_pwm=pwm_enabled,
                           gpio=gpio,
                           pwm=pwm)
        self.motors = [self._M1, self._M2]
        # Initialise Motors
        self.setBrakes(0,0)
        self._gpio = gpio
        

    ###
    ###  B R A K I N G
    ###
    def setM1Brake(self, brake):
        self._M1.setBrake(brake)

    def setM2Brake(self, brake):
        self._M2.setBrake(brake)

    def setBrakes(self, m1Brake, m2Brake):
        self.setM1Brake(m1Brake)
        self.setM2Brake(m2Brake)

    ###
    ###  S P E E D
    ###
    def setM1Speed(self, speed):
        self._M1.setSpeed(speed)

    def setM2Speed(self, speed):
        self._M2.setSpeed(speed)

    def setSpeeds(self, m1Speed, m2Speed):
        self.setM1Speed(m1Speed)
        self.setM2Speed(m2Speed)

    ###
    ###  O T H E R
    ### 
    def getMotor(self, num):
        if (num < 1) or (num > 4):
            raise NameError('Shield Motor must be between 1 and 2 inclusive')

        return self.motors[num-1]

    def cleanup(self):
        self._gpio.cleanup()
