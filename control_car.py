import curses
import time

import RPi.GPIO as GPIO

MOTOR_RIGHT_IN1 = 31
MOTOR_RIGHT_IN2 = 29
MOTOR_RIGHT_ENABLE = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOR_RIGHT_IN1, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_IN2, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_ENABLE, GPIO.OUT)

PWM_RIGHT_ENABLE = GPIO.PWM(MOTOR_RIGHT_ENABLE, 1000)  # 1Khz
PWM_RIGHT_ENABLE.start(0)

GPIO.output(MOTOR_RIGHT_IN1, GPIO.LOW)
GPIO.output(MOTOR_RIGHT_IN2, GPIO.LOW)
PWM_RIGHT_ENABLE.ChangeDutyCycle(0)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()

screen.timeout(500)
screen.keypad(True)

PWM_DUTY_CYCLE_PERCENT = 50

try:
    while True:

        char = screen.getch()
        print(char)
        if char == ord('q'):
            break
        elif char == curses.KEY_UP:
            print("up")
            GPIO.output(MOTOR_RIGHT_IN1, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_IN2, GPIO.LOW)
            PWM_RIGHT_ENABLE.ChangeDutyCycle(PWM_DUTY_CYCLE_PERCENT)
        elif char == curses.KEY_DOWN:
            print("down")
            GPIO.output(MOTOR_RIGHT_IN1, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_IN2, GPIO.HIGH)
            PWM_RIGHT_ENABLE.ChangeDutyCycle(PWM_DUTY_CYCLE_PERCENT)
        elif char == curses.KEY_RIGHT:
            print("right")
        elif char == curses.KEY_LEFT:
            print("left")
        elif char == curses.KEY_PPAGE:
            print("DUTY CYCLE " + str(PWM_DUTY_CYCLE_PERCENT))
            PWM_DUTY_CYCLE_PERCENT += 1
            if PWM_DUTY_CYCLE_PERCENT > 100:
                PWM_DUTY_CYCLE_PERCENT = 100
            time.sleep(0.5)
        elif char == curses.KEY_NPAGE:
            print("DUTY CYCLE " + str(PWM_DUTY_CYCLE_PERCENT))
            PWM_DUTY_CYCLE_PERCENT -= 1
            if PWM_DUTY_CYCLE_PERCENT <= 0:
                PWM_DUTY_CYCLE_PERCENT = 1
            time.sleep(0.5)
        else:
            print("stop motor")
            GPIO.output(MOTOR_RIGHT_IN1, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_IN2, GPIO.LOW)
            PWM_RIGHT_ENABLE.ChangeDutyCycle(0)

finally:
    # Close down curses properly, inc turn echo back on!
    curses.nocbreak();
    screen.keypad(0);
    curses.echo()
    curses.endwin()

    GPIO.output(MOTOR_RIGHT_IN1, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_IN2, GPIO.LOW)
    PWM_RIGHT_ENABLE.ChangeDutyCycle(0)
