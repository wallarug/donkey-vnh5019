#!/usr/python3

#
#  Tests for Pololu Motor Driver
#
#
#  Updated: 05/09/2017

import time




#
#   TEST GROUPS 
#
def testBasic():
    try:
        import Pololu_VNH5019 as VNH
    except:
        print("Error: cannot import driver!")
        return

    mh = VNH.Pololu_DualVNH5019Shield()

    print("*************************")
    print("* Basic Motor Testings  *")
    print("*************************")

    testM1Basic(mh)
    testM2Basic(mh)

    # Clean up GPIO
    mh.cleanup()

    
    print("Basic testing COMPLETE!")

def testCoordination():
    try:
        import Pololu_VNH5019 as VNH
    except:
        print("Error: cannot import driver!")
        return

    mh = VNH.Pololu_DualVNH5019Shield()

    print("*************************")
    print("* Coordindation Testing *")
    print("*************************")

    testForwardCoordination(mh)
    testBackwardCoordination(mh)

    # Clean up GPIO
    mh.cleanup()

    print("Coordindation testing COMPLETE!")


def testBrakes():
    try:
        import Pololu_VNH5019 as VNH
    except:
        print("Error: cannot import driver!")
        return

    mh = VNH.Pololu_DualVNH5019Shield()

    print("*************************")
    print("*     Brake Testing     *")
    print("*************************")

    testM1Brake(mh)
    testM2Brake(mh)
    testM1M2Brake(mh)

    # Clean up GPIO
    mh.cleanup()

    print("Brake testing COMPLETE!")

    
    

########################################
##      UNIT TESTS (BY PART)          ##   
########################################

def testM1Basic(mh):
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


def testM2Basic(mh):
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

def testForwardCoordination(mh):
    """
        Test that both motors move in same direction
    """
    
    print(" [ F O R W A R D S ] ")

    percent = 0
    for i in range(400):
        mh.setSpeeds(i, i)
        percent = i / 4
        print("speed: {0}%".format(round(percent,2)))
        time.sleep(0.05)

    time.sleep(3)

    for i in range(400, 0, -1):
        mh.setSpeeds(i, i)
        percent = i / 4
        print("speed: {0}%".format(round(percent,2)))
        time.sleep(0.05)

    print("SLEEPING FOR 3 SECONDS")
    time.sleep(3)


def testBackwardCoordination(mh):
    """
        Test that both motors move in same direction
    """
    
    print(" [ B A C K W A R D S] ")

    percent = 0
    for i in range(0, -400, -1):
        mh.setSpeeds(i, i)
        percent = i / 4
        print("speed: {0}%".format(round(percent,2)))
        time.sleep(0.05)

    time.sleep(3)

    for i in range(-400, 0, 1):
        mh.setSpeeds(i, i)
        percent = i / 4
        print("speed: {0}%".format(round(percent,2)))
        time.sleep(0.05)

    print("SLEEPING FOR 3 SECONDS")
    time.sleep(3)
            
def testM1Brake(mh):
    """
        Test that the brake code works (not normally used)
    """
    
    print(" [ F O R W A R D S ] ")

    percent = 80
    mh.setM1Speed(80*4)

    print("speed: {0}%".format(round(percent,2)))
    time.sleep(3)

    print(" [ A P P L Y I N G   B R A K E ] ")
    time.sleep(1)

    mh.setM1Brake(100)
    
    print("SLEEPING FOR 3 SECONDS")
    time.sleep(3)

def testM2Brake(mh):
    """
        Test that the brake code works (not normally used)
    """
    
    print(" [ F O R W A R D S ] ")

    percent = 80
    mh.setM2Speed(80*4)

    print("speed: {0}%".format(round(percent,2)))
    time.sleep(3)

    print(" [ A P P L Y I N G   B R A K E ] ")
    time.sleep(1)

    mh.setM2Brake(100)
    
    print("SLEEPING FOR 3 SECONDS")
    time.sleep(3)    
    

def testM1M2Brake(mh):
    """
        Test that the brake code works (not normally used)
    """
    
    print(" [ F O R W A R D S ] ")

    percent = 80
    mh.setSpeeds(80*4, 80*4)

    print("speed: {0}%".format(round(percent,2)))
    time.sleep(3)

    print(" [ A P P L Y I N G   B R A K E ] ")
    time.sleep(1)

    mh.setBrakes(100,100)
    
    print("SLEEPING FOR 3 SECONDS")
    time.sleep(3)

    

def __name__():
    basic()

testBrakes()
