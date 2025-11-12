import sys
import os


import time
import RPi.GPIO as GPIO

RPWM_PIN = 3
LPWM_PIN = 4
	
GPIO.setmode(GPIO.BCM)
GPIO.setup(RPWM_PIN, GPIO.OUT)
GPIO.setup(LPWM_PIN, GPIO.OUT)

pwm_forward = GPIO.PWM(RPWM_PIN, 1000)
pwm_reverse = GPIO.PWM(LPWM_PIN, 1000)
pwm_forward.start(0)
pwm_reverse.start(0)
try:
	print("Spin forward 10", end="\n")
	pwm_forward.ChangeDutyCycle(10)
	time.sleep(2)
	
	print("Spin forward 25", end="\n")
	pwm_forward.ChangeDutyCycle(25)
	time.sleep(2)

	print("stop forward 50")
	pwm_forward.ChangeDutyCycle(50)
	time.sleep(1)
	
	print("Spin forward 100", end="\n")
	pwm_forward.ChangeDutyCycle(100)
	time.sleep(2)

	print("stop forward")
	pwm_forward.ChangeDutyCycle(0)
	
	
	print("Spin backwards", end="\n")
	pwm_reverse.ChangeDutyCycle(100)
	time.sleep(2)
	
	print("stop backwards")
	pwm_reverse.ChangeDutyCycle(0)
	time.sleep(1)
	
	
except KeyboardInterrupt:
	print("Test ended")
	
finally:
	pwm_forward.stop()
	pwm_reverse.stop()
	GPIO.cleanup()
