import curses

import RPi.GPIO as GPIO

MOTOR_RIGHT_IN1 = 29
MOTOR_RIGHT_IN2 = 31
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
screen.timeout(1000)
screen.keypad(True)

try:
    while True:

        char = screen.getch()

        if char == ord('q'):
            break
        elif char == curses.KEY_UP:
            print("up")
            GPIO.output(MOTOR_RIGHT_IN1, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_IN2, GPIO.LOW)
            PWM_RIGHT_ENABLE.ChangeDutyCycle(50)
        elif char == curses.KEY_DOWN:
            print("down")
            GPIO.output(MOTOR_RIGHT_IN1, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_IN2, GPIO.HIHG)
            PWM_RIGHT_ENABLE.ChangeDutyCycle(50)
        elif char == curses.KEY_RIGHT:
            print("right")
        elif char == curses.KEY_LEFT:
            print("left")
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
