# coding=utf-8
import Jetson.GPIO as GPIO
import time

class Turntable():
    def __init__(self):
        # self.RX_JETSON = 25 # cable verde 25 EN BCM en pines de lsa Jetson es el 22 del conector j21
        # self.TX_JETSON = 24 # cable blanco 24 EN BCM en pines de lsa Jetson es el 18 del conector j21

        self.RX_JETSON = 24 # cable blanco 24 EN BCM en pines de lsa Jetson es el 18 del conector j21
        self.TX_JETSON = 25 # cable verde 25 EN BCM en pines de lsa Jetson es el 22 del conector j21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TX_JETSON, GPIO.OUT, initial=GPIO.LOW) 
        GPIO.setup(self.RX_JETSON, GPIO.IN)

    def turn(self):
        print("inicio rotacion")
        GPIO.output(self.TX_JETSON, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(self.TX_JETSON, GPIO.LOW)
        time.sleep(0.5)
        while (not GPIO.input(self.RX_JETSON)):
            pass
        print("fin rotacion")


# step_grade = int(input('Ingrese los  pasos en grados [6, 12, 18, 24, 30, 36, 60, 72, 90, 120, 180, 360]: '))
# step = int(step_grade * 60 / 360)

