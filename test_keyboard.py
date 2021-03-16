import curses

import RPi.GPIO as GPIO
PIN_LED = 12
GPIO.setmode(GPIO.BOARD)  # set pin numbering system
GPIO.setup(PIN_LED, GPIO.OUT)

# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    while True:
        char = screen.getch()
        if char == ord('q'):
            break
        elif char == curses.KEY_UP:
            print("up")
            GPIO.output(PIN_LED, GPIO.HIGH)
        elif char == curses.KEY_DOWN:
            print("down")
            GPIO.output(PIN_LED, GPIO.LOW)
        elif char == curses.KEY_RIGHT:
            print("right")
        elif char == curses.KEY_LEFT:
            print("left")
        elif char == 10:
            print("stop")

finally:
    # Close down curses properly, inc turn echo back on!
    curses.nocbreak();
    screen.keypad(0);
    curses.echo()
    curses.endwin()
