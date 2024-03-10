import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo_pin = 13
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)
angle = 0.0000

def calculate_duty_cycle(angle):
    return angle * 0.55556

def rot(change, angle):
    duty_cycle = round(calculate_duty_cycle(angle+change),2)+2
    print(duty_cycle)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(duty_cycle*0.003)


def rotate_servo(speed, duration):
    duty_cycle_increment = speed / 10.0
    duty_cycle = 0

    try:
        while True:
            # Increase duty cycle for forward rotation
            for angle in range(0, 9):
                duty_cycle = round(calculate_duty_cycle(angle),2)+2
                print(duty_cycle)
                pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(duration)

            # Decrease duty cycle for backward rotation
            for angle in range(9, 0, -1):
                duty_cycle = round(calculate_duty_cycle(angle),2)+2
                print(duty_cycle)
                pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(duration)

    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()

speed = 5  # Adjust the speed (degrees per second) as needed
duration = 0.06  # Adjust the duration of each step as needed
rotate_servo(speed, duration)
