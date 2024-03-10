import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo_pin = 13
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def angle_to_duty(angle):
    min_duty = 26
    max_duty = 128
    print("angle_to_duty")
    return (min_duty + (angle / 180.0) * (max_duty - min_duty)) / 10

pwm.ChangeDutyCycle(angle_to_duty(45))
time.sleep(1)

while True:
    print("loop")
    pwm.ChangeDutyCycle(angle_to_duty(0))
    print(0)
    time.sleep(0.4)
    pwm.ChangeDutyCycle(angle_to_duty(45))
    print(45)
    time.sleep(0.4)
    pwm.ChangeDutyCycle(angle_to_duty(90))
    print(90)
    time.sleep(0.4)
    pwm.ChangeDutyCycle(angle_to_duty(45))
    print(45)
    time.sleep(0.4)
