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



class VNH5019(object):
    """ Polulu VNH5019 Motor Controller. """

    def __init__(self, EN, INA, INB, PWM):
        self._directionA = INA
        self._directionB = INB
        self._enable = EN
        self._speed = PWM

        
