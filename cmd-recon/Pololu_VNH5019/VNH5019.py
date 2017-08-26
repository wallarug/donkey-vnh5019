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
                 enable_pwm=enable_pwm,
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
            gpio.setup(pin, GPIO.OUT)

        # Setup the PWM speed control
        if ( enable_pwm ):
            pwm.start(ctrl, 0)
        else:
            gpio.setup(ctrl, GPIO.OUT)
            self._gpio.output(ctrl, False)

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

        if ( self._enabled_pwm ):
            self._pwm.set_duty_cycle(self._ctrl, speed / 4)
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
        
        

class DualVNH5019MotorShield(object):
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
        self._M1 = VNH5019(m1ina,
                           m1inb,
                           m1en,
                           m1pwm,
                           enabled_pwm=pwm_enabled,
                           gpio=gpio,
                           pwm=pwm)
        self._M2 = VNH5019(m2ina,
                           m2inb,
                           m2en,
                           m2pwm,
                           enabled_pwm=pwm_enabled,
                           gpio=gpio,
                           pwm=pwm)
        # Initialise Motors
        setBrakes(0)
        

    ###
    ###  B R A K I N G
    ###
    def setM1Brake(brake):
        self._M1.setBrake(brake)

    def setM2Brake(brake):
        self._M2.setBrake(brake)

    def setBrakes(m1Brake, m2Brake):
        setM1Brake(m1Brake)
        setM2Brake(m2Brake)

    ###
    ###  S P E E D
    ###
    def setM1Speed(speed):
        self._M1.setSpeed(speed)

    def setM2Brake(speed):
        self._M2.setSpeed(speed)

    def setSpeeds(m1Speed, m2Speed):
        setM1Speed(m1Speed)
        setM2Speed(m2Speed)

    