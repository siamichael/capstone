import sys
import os

import time
import RPi.GPIO as GPIO

RPWM_PIN = 9
LPWM_PIN = 11


def ramp_speed(pwm_object, start_speed, end_speed, duration=0.3):    
    steps = 20
    delay = duration / steps
    
    for i in range(steps + 1):
        current_speed = start_speed + (end_speed - start_speed) * (i / steps)
        pwm_object.ChangeDutyCycle(int(current_speed))
        time.sleep(delay)

	
GPIO.setmode(GPIO.BCM)
GPIO.setup(RPWM_PIN, GPIO.OUT)
GPIO.setup(LPWM_PIN, GPIO.OUT)

GPIO.output(RPWM_PIN, GPIO.LOW)
GPIO.output(LPWM_PIN, GPIO.LOW)

pwm_forward = GPIO.PWM(RPWM_PIN, 1000)
pwm_reverse = GPIO.PWM(LPWM_PIN, 1000)
pwm_forward.start(0)
pwm_reverse.start(0)

try:
	"""
	print("Spin forward", end="\n")
	pwm_forward.ChangeDutyCycle(100)
	time.sleep(2)

	print("stop forward")
	pwm_forward.ChangeDutyCycle(0)
	time.sleep(1)
	
	
	print("Spin backwards", end="\n")
	pwm_reverse.ChangeDutyCycle(100)
	time.sleep(2)
	
	print("stop backwards")
	pwm_reverse.ChangeDutyCycle(0)
	time.sleep(1)
	"""
	
	print("Spin forward")
	ramp_speed(pwm_forward, start_speed=0, end_speed=100, duration=0.3)
	time.sleep(2)

	print("stop forward (with ramp)")
	ramp_speed(pwm_forward, start_speed=100, end_speed=0, duration=0.3)
	time.sleep(1)
    
	print("Spin backwards")
	ramp_speed(pwm_reverse, start_speed=0, end_speed=100, duration=0.3)
	time.sleep(2)
    
	print("stop backwards (with ramp)")
	ramp_speed(pwm_reverse, start_speed=100, end_speed=0, duration=0.3)
	time.sleep(1)
	
	
except KeyboardInterrupt:
	print("Test ended")
	
finally:
	pwm_forward.stop()
	pwm_reverse.stop()
	GPIO.cleanup()
