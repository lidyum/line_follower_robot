import RPi.GPIO as GPIO
from time import sleep

PIN_LED = 35
GPIO.setmode(GPIO.BOARD)  # set pin numbering system
GPIO.setup(PIN_LED, GPIO.OUT)
pi_pwm = GPIO.PWM(PIN_LED, 1000)  # 1Khz
pi_pwm.start(0)  # start PWM of required Duty Cycle

while True:
    for duty in range(0, 101, 1):
        pi_pwm.ChangeDutyCycle(duty)
        sleep(0.01)
    sleep(0.5)

    for duty in range(100, -1, -1):
        pi_pwm.ChangeDutyCycle(duty)
        sleep(0.01)
    sleep(0.5)
