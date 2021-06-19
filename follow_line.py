import curses
import time

import RPi.GPIO as GPIO

MOTOR_RIGHT_IN1 = 31
MOTOR_RIGHT_IN2 = 29
MOTOR_RIGHT_ENABLE = 33
SENSOR_RIGHT = 37

MOTOR_LEFT_IN1 = 38
MOTOR_LEFT_IN2 = 40
MOTOR_LEFT_ENABLE = 32
SENSOR_LEFT = 36

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOR_RIGHT_IN1, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_IN2, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_ENABLE, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_IN1, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_IN2, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_ENABLE, GPIO.OUT)

GPIO.setup(SENSOR_RIGHT, GPIO.IN)
GPIO.setup(SENSOR_LEFT, GPIO.IN)

PWM_RIGHT_ENABLE = GPIO.PWM(MOTOR_RIGHT_ENABLE, 1000)  # 1Khz
PWM_RIGHT_ENABLE.start(0)

PWM_LEFT_ENABLE = GPIO.PWM(MOTOR_LEFT_ENABLE, 1000)  # 1Khz
PWM_LEFT_ENABLE.start(0)

GPIO.output(MOTOR_RIGHT_IN1, GPIO.LOW)
GPIO.output(MOTOR_RIGHT_IN2, GPIO.LOW)
PWM_RIGHT_ENABLE.ChangeDutyCycle(0)

GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)
PWM_LEFT_ENABLE.ChangeDutyCycle(0)

PWM_DUTY_CYCLE_MINIMUM_PERCENT = 50
PWM_DUTY_CYCLE_MAXIMUM_PERCENT = 100
PWM_DUTY_CYCLE_PERCENT = 30


def left_motor_forward():
    GPIO.output(MOTOR_LEFT_IN1, GPIO.HIGH)
    GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)
    PWM_LEFT_ENABLE.ChangeDutyCycle(PWM_DUTY_CYCLE_PERCENT)



def left_motor_stop():
    GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)
    PWM_LEFT_ENABLE.ChangeDutyCycle(0)


def left_motor_backward():
    GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_IN2, GPIO.HIGH)
    PWM_LEFT_ENABLE.ChangeDutyCycle(PWM_DUTY_CYCLE_PERCENT)


def right_motor_forward():
    GPIO.output(MOTOR_RIGHT_IN1, GPIO.HIGH)
    GPIO.output(MOTOR_RIGHT_IN2, GPIO.LOW)
    PWM_RIGHT_ENABLE.ChangeDutyCycle(PWM_DUTY_CYCLE_PERCENT)


def right_motor_stop():
    GPIO.output(MOTOR_RIGHT_IN1, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_IN2, GPIO.LOW)
    PWM_RIGHT_ENABLE.ChangeDutyCycle(0)


def right_motor_backward():
    GPIO.output(MOTOR_RIGHT_IN1, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_IN2, GPIO.HIGH)
    PWM_RIGHT_ENABLE.ChangeDutyCycle(PWM_DUTY_CYCLE_PERCENT)


try:
    while True:
        is_right_on_line = GPIO.input(SENSOR_RIGHT)
        is_left_on_line = GPIO.input(SENSOR_LEFT)
        if (is_right_on_line and is_left_on_line) or (not is_right_on_line and not is_left_on_line):
            right_motor_forward()
            left_motor_forward()
        elif is_right_on_line:
            right_motor_stop()
        elif is_left_on_line:
            left_motor_stop()
except:
    GPIO.cleanup()
