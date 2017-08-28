# Modifications for actuators.py
#
# Author: Cian Byrne (wallarug)
#
# **Instructions **
# Copy this into the donkeycar/parts/actuators/actuators.py
#  file from the donkey (@wroscoe) respository to enable
#  support for the VNH5019 Duel Motor Shield Controller.
#
#

def Pololu_DualVNH5019:
    '''
    Pololu Dual VNH5019 Motor Driver
    Used for both motors on tank track.
    '''
    def __init__(self):
        from Pololu_VNH5019 import Pololu_DualVNH5019Shield
        import Adafruit_GPIO as GPIO
        import Adafruit_GPIO.PWM as PWM

        self.mh = Pololu_DualVNH5019Shield(gpio=GPIO, pwm=PWM)

        self.speed = 0
        self.throttle = 0

    def run(self, speed):
        '''
        Update the speed of the motor where 1 is full forward and
        -1 is full backwards.
        '''
        if speed > 1 or speed < -1:
            raise ValueError( "Speed must be between 1(forward) and -1(reverse)")

        self.speed = speed
        self.throttle = int(utils.map_range(abs(speed), -1, 1, -400, 400))

        self.mh.setSpeeds(self.throttle, self.throttle)

    def shutdown(self):
        self.mh.setBrakes(0)


def Tank:
    '''
    Pololu Dual VNH5019 Motor Driver
    Used for both motors on tank track.
    '''
    def __init__(self):
        from Pololu_VNH5019 import Pololu_DualVNH5019Shield
        import Adafruit_GPIO as GPIO
        import Adafruit_GPIO.PWM as PWM

        self.mh = Pololu_DualVNH5019Shield(gpio=GPIO, pwm=PWM)

        self.speed = 0
        self.throttleL = 0
        self.throttleR = 0


    def run(self, steering, throttle):
        '''
        Update the speed of the motor where 1 is full forward and
        -1 is full backwards.
        '''

        if throttle > 1 or throttle < -1:
            raise ValueError( "Speed must be between 1(forward) and -1(reverse)")

        if steering > 1 or steering < -1:
            raise ValueError( "Steering must be between 1 and -1")

        if ( steering > 0 and throttle > 0 ):       # Quadrant 1
            self.throttleL = self.convert(throttle)
            self.throttleR = self.convert(throttle-steering)

        elif ( steering < 0 and throttle > 0 ):     # Quadrant 2
            self.throttleL = self.convert(throttle+steering)
            self.throttleR = self.convert(throttle)

        elif ( steering > 0 and throttle < 0 ):     # Quadrant 4
            self.throttleL = self.convert(throttle)
            self.throttleR = self.convert(throttle+steering)

        elif ( steering < 0 and throttle < 0 ):     # Quadrant 3
            self.throttleL = self.convert(throttle-steering)
            self.throttleR = self.convert(throttle)
        
        
        self.mh.setSpeeds(self.throttleL, self.throttleR)


    def shutdown(self):
        self.mh.setBrakes(0)


    def convert(self, value):
        return int(utils.map_range(abs(value), -1, 1, -400, 400))
