#!/usr/python3

#
#  Tests for Pololu Motor Driver
#
#
#  Updated: 05/09/2017

import time

def basic():
    try:
        import Pololu_VNH5019 as VNH
    except:
        print("Error: cannot import driver!")
        return

    mh = VNH.Pololu_DualVNH5019Shield()


    ##
    ##  M1 Tests - Direction, Speed
    ##
    print("Testing motor 1..")
    print("[forwards @ 25%]")
    mh.setM1Speed(100)
    time.sleep(3)

    print("[forwards @ 50%]")
    mh.setM1Speed(200)
    time.sleep(3)

    print("[forwards @ 75%]")
    mh.setM1Speed(300)
    time.sleep(3)

    print("[forwards @ 100%]")
    mh.setM1Speed(400)
    time.sleep(3)

    print("[speed stop]")
    mh.setM1Speed(0)
    time.sleep(3)

    print("[backwards @ 50%]")
    mh.setM1Speed(-200)
    time.sleep(3)

    print("[backwards @ 100%]")
    mh.setM1Speed(-400)
    time.sleep(3)

    print("[speed stop]")
    mh.setM1Speed(0)
    time.sleep(3)


    ##
    ##  M2 Tests - Direction, Speed
    ##
    print("Testing motor 2..")
    print("[forwards @ 25%]")
    mh.setM2Speed(100)
    time.sleep(3)

    print("[forwards @ 50%]")
    mh.setM2Speed(200)
    time.sleep(3)

    print("[forwards @ 75%]")
    mh.setM2Speed(300)
    time.sleep(3)

    print("[forwards @ 100%]")
    mh.setM2Speed(400)
    time.sleep(3)

    print("[speed stop]")
    mh.setM2Speed(0)
    time.sleep(3)

    print("[backwards @ 50%]")
    mh.setM2Speed(-200)
    time.sleep(3)

    print("[backwards @ 100%]")
    mh.setM2Speed(-400)
    time.sleep(3)

    print("[speed stop]")
    mh.setM2Speed(0)
    time.sleep(3)
    

    print("Basic testing complete!")


def brake():
    pass    
    
    
