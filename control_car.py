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

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()

screen.timeout(400)
screen.keypad(True)

PWM_DUTY_CYCLE_MINIMUM_PERCENT = 50
PWM_DUTY_CYCLE_MAXIMUM_PERCENT = 100
PWM_DUTY_CYCLE_PERCENT = 50


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

        char = screen.getch()
        print(char)
        if char == ord('O') or char == ord('o'):
            while True:
                if char == ord('Q') or char == ord('q'):
                    break
                else:
                    is_right_on_line = GPIO.input(SENSOR_RIGHT)
                    is_left_on_line = GPIO.input(SENSOR_LEFT)
                    if is_right_on_line:
                        left_motor_forward()
                        right_motor_stop()
                        print("RIGHT SENSOR ONLINE")
                    elif is_left_on_line:
                        right_motor_forward()
                        left_motor_stop()
                        print("LEFT SENSOR ONLINE")
                    else:
                        right_motor_stop()
                        left_motor_stop()
        else:
            if char == curses.KEY_UP:
                print("up")
                left_motor_forward()
                right_motor_forward()
            elif char == curses.KEY_DOWN:
                print("down")
                left_motor_backward()
                right_motor_backward()
            elif char == curses.KEY_RIGHT:
                print("right")
                left_motor_forward()
                right_motor_stop()
            elif char == curses.KEY_LEFT:
                print("left")
                right_motor_forward()
                left_motor_stop()
            elif char == curses.KEY_PPAGE:
                print("DUTY CYCLE " + str(PWM_DUTY_CYCLE_PERCENT))
                PWM_DUTY_CYCLE_PERCENT += 1
                if PWM_DUTY_CYCLE_PERCENT >= PWM_DUTY_CYCLE_MAXIMUM_PERCENT:
                    PWM_DUTY_CYCLE_PERCENT = PWM_DUTY_CYCLE_MAXIMUM_PERCENT
                time.sleep(0.1)
            elif char == curses.KEY_NPAGE:
                print("DUTY CYCLE " + str(PWM_DUTY_CYCLE_PERCENT))
                PWM_DUTY_CYCLE_PERCENT -= 1
                if PWM_DUTY_CYCLE_PERCENT <= PWM_DUTY_CYCLE_MINIMUM_PERCENT:
                    PWM_DUTY_CYCLE_PERCENT = PWM_DUTY_CYCLE_MINIMUM_PERCENT
                time.sleep(0.1)
            else:
                print("stop motor")
                left_motor_stop()
                right_motor_stop()

finally:
    # Close down curses properly, inc turn echo back on!
    curses.nocbreak();
    screen.keypad(0);
    curses.echo()
    curses.endwin()

    left_motor_stop()
    right_motor_stop()
