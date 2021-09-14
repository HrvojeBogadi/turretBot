import RPi.GPIO as GPIO
import time

def shoot(theta, rho):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)

    pwm1 = GPIO.PWM(13, 50)
    pwm2 = GPIO.PWM(12, 50)
    pwm1.start(0)
    pwm2.start(0)
    GPIO.output(17, GPIO.HIGH)
    duty_c1 = 7.5-rho/90*5
    duty_c2 = 7.5-theta/90*5
    pwm1.ChangeDutyCycle(duty_c1)
    pwm2.ChangeDutyCycle(duty_c2)
    time.sleep(1)
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    time.sleep(9)
    GPIO.output(17, GPIO.LOW)

    
    pwm1.stop()
    pwm2.stop()

    GPIO.cleanup()