import curses

import RPi.GPIO as GPIO

MOTOR_LEFT_IN1 = 38
MOTOR_LEFT_IN2 = 40
GPIO.setmode(GPIO.BOARD)  # set pin numbering system
GPIO.setup(MOTOR_LEFT_IN1, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_IN2, GPIO.OUT)

GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.timeout(1000)
screen.keypad(True)

try:
    while True:

        char = screen.getch()

        if char == ord('q'):
            break
        elif char == curses.KEY_UP:
            print("up")
            GPIO.output(MOTOR_LEFT_IN1, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)
        elif char == curses.KEY_DOWN:
            print("down")
            GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_IN2, GPIO.HIGH)
        elif char == curses.KEY_RIGHT:
            print("right")
        elif char == curses.KEY_LEFT:
            print("left")
        elif char == 10:
            print("stop")
        else:
            print("stop motor")
            GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)

finally:
    # Close down curses properly, inc turn echo back on!
    curses.nocbreak();
    screen.keypad(0);
    curses.echo()
    curses.endwin()
