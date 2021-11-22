# coding=utf-8
import Jetson.GPIO as GPIO
from time import sleep

STP = 18
DIR = 24
ENB = 25

STEPS_PER_REV_BASE = 1300
STEPS_PER_REV_MOTOR = 96
# t = float(input('Periodo en S: '))
# steps = int(input('grados por paso: '))
# steps = grados/1.8

def sense_step(step_number_per_angle, period=1000):

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(STP, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(DIR, GPIO.OUT, initial=GPIO.LOW)

    try:
        # print('Para finalizar precione ctrl+c')
        GPIO.output(DIR, GPIO.LOW)
        for paso in range(step_number_per_angle):
            GPIO.output(STP, GPIO.HIGH)
            sleep(1/period)
            GPIO.output(STP, GPIO.LOW)
            sleep(1/period)
        # input('pasos dados: '+ str() + ' --ENTER')
        # print('MEDICION')
        # sleep(2)
    except KeyboardInterrupt:
        print('Ejecucuion Finalizada')

    finally:
        GPIO.cleanup()
        print('Puertos disponbles')

def main():
    while 1:
        periodo = int(input('Perioso: '))
        sense_step(1300, period=periodo)


if __name__ == '__main__':
    main()