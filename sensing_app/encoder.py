# coding=utf-8
import Jetson.GPIO as GPIO
from time import sleep

encoA = 27
encoB = 22

def get_encoder(prev_val, counter=0):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(encoA, GPIO.IN)
    GPIO.setup(encoB, GPIO.IN)
    

    actual_val = GPIO.input(encoA)

    if (actual_val != prev_val):
        if (GPIO.input(encoB) != actual_val):
            counter += 1
        else:
            counter -= 1

    prev_val = actual_val
    return prev_val, counter


def initial_state():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(encoA, GPIO.IN)
    return GPIO.input(encoA)

def prove_pins():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(encoA, GPIO.IN)
    GPIO.setup(encoB, GPIO.IN)

    print('pin A:', GPIO.input(encoA), '----', 'pin B:', GPIO.input(encoB))

def main():
    initial_val = initial_state()
    prev_val, pos = get_encoder(initial_val)

    while 1:
        prev_val, pos = get_encoder(prev_val, pos)
        print(pos)
        # sleep(1)


if __name__ == '__main__':
    main()