from RPi import GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)

for _ in range(50):
    GPIO.output(8, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(8, GPIO.LOW)
    time.sleep(1)
