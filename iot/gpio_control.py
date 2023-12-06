import RPi.GPIO as GPIO
TV_GPIO_N = 4
LIGHT_GPIO_N = 17
AC_GPIO_L1 = 5
AC_GPIO_L2 = 6
AC_GPIO_L3 = 13
AC_GPIO_L4 = 19
BLIND_GPIO_L1 = 18
BLIND_GPIO_L2 = 23
BLIND_GPIO_L3 = 24
BLIND_GPIO_L4 = 25


def GPIO_INIT() :
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TV_GPIO_N,GPIO.OUT)
    GPIO.setup(LIGHT_GPIO_N,GPIO.OUT)
    GPIO.setup(AC_GPIO_L1,GPIO.OUT)
    GPIO.setup(AC_GPIO_L2,GPIO.OUT)
    GPIO.setup(AC_GPIO_L3,GPIO.OUT)
    GPIO.setup(AC_GPIO_L4,GPIO.OUT)
    GPIO.setup(BLIND_GPIO_L1,GPIO.OUT)
    GPIO.setup(BLIND_GPIO_L2,GPIO.OUT)
    GPIO.setup(BLIND_GPIO_L3,GPIO.OUT)
    GPIO.setup(BLIND_GPIO_L4,GPIO.OUT)

def GPIO_SET(dev, val) :
    print(f"In GPIO_SET {dev} {val}")
    if dev == "TV" :
        if val == 0 : GPIO.output(TV_GPIO_N, False)
        else : GPIO.output(TV_GPIO_N, True)
    elif dev == "light" :
        if val == 0 : GPIO.output(LIGHT_GPIO_N, False)
        else : GPIO.output(LIGHT_GPIO_N, True)
    elif dev == "AC" :
        if val == 0 :
            GPIO.output(AC_GPIO_L1, False)
            GPIO.output(AC_GPIO_L2, False)
            GPIO.output(AC_GPIO_L3, False)
            GPIO.output(AC_GPIO_L4, False)
        elif val == 1 :
            GPIO.output(AC_GPIO_L1, True)
            GPIO.output(AC_GPIO_L2, False)
            GPIO.output(AC_GPIO_L3, False)
            GPIO.output(AC_GPIO_L4, False)
        elif val == 2 :
            GPIO.output(AC_GPIO_L1, False)
            GPIO.output(AC_GPIO_L2, True)
            GPIO.output(AC_GPIO_L3, False)
            GPIO.output(AC_GPIO_L4, False)
        elif val == 3 :
            GPIO.output(AC_GPIO_L1, False)
            GPIO.output(AC_GPIO_L2, False)
            GPIO.output(AC_GPIO_L3, True)
            GPIO.output(AC_GPIO_L4, False)
        elif val == 4 :
            GPIO.output(AC_GPIO_L1, False)
            GPIO.output(AC_GPIO_L2, False)
            GPIO.output(AC_GPIO_L3, False)
            GPIO.output(AC_GPIO_L4, True)
    elif dev == "blind" :
        if val == 0 :
            GPIO.output(BLIND_GPIO_L1, False)
            GPIO.output(BLIND_GPIO_L2, False)
            GPIO.output(BLIND_GPIO_L3, False)
            GPIO.output(BLIND_GPIO_L4, False)
        elif val == 1 :
            GPIO.output(BLIND_GPIO_L1, True)
            GPIO.output(BLIND_GPIO_L2, False)
            GPIO.output(BLIND_GPIO_L3, False)
            GPIO.output(BLIND_GPIO_L4, False)
        elif val == 2 :
            GPIO.output(BLIND_GPIO_L1, False)
            GPIO.output(BLIND_GPIO_L2, True)
            GPIO.output(BLIND_GPIO_L3, False)
            GPIO.output(BLIND_GPIO_L4, False)
        elif val == 3 :
            GPIO.output(BLIND_GPIO_L1, False)
            GPIO.output(BLIND_GPIO_L2, False)
            GPIO.output(BLIND_GPIO_L3, True)
            GPIO.output(BLIND_GPIO_L4, False)
        elif val == 4 :
            GPIO.output(BLIND_GPIO_L1, False)
            GPIO.output(BLIND_GPIO_L2, False)
            GPIO.output(BLIND_GPIO_L3, False)
            GPIO.output(BLIND_GPIO_L4, True)


# GPIO_INIT()
# GPIO.output(TV_GPIO_N, False)
# GPIO.output(LIGHT_GPIO_N, False)
# GPIO.output(AC_GPIO_L1, False)
# GPIO.output(AC_GPIO_L2, False)
# GPIO.output(AC_GPIO_L3, False)
# GPIO.output(AC_GPIO_L4, False)
# GPIO.output(BLIND_GPIO_L1, False)
# GPIO.output(BLIND_GPIO_L2, False)
# GPIO.output(BLIND_GPIO_L3, False)
# GPIO.output(BLIND_GPIO_L4, False)