import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from motor_driver import MotorDriver
import RPi.GPIO as GPIO

RPWM_PIN = 3
LPWM_PIN = 4
	
GPIO.setmode(GPIO.BCM)
GPIO.setup(RPWM_PIN, GPIO.OUT)
GPIO.setup(LPWM_PIN, GPIO.OUT)
pwm_forward = GPIO.PWM(RPWM_PIN, 10000)
pwm_reverse = GPIO.PWM(LPWM_PIN, 10000)
pwm_forward.start(0)
pwm_reverse.start(0)
try:
	print("Spin forward", end="\n")
	pwm_forward.ChangeDutyCycle(100)
	time.sleep(2)

	pwm_forward.ChangeDutyCycle(0)
	time.sleep(1)
	
	print("Spin backwards", end="\n")
	pwm_reverse.ChangeDutyCycle(100)
	time.sleep(2)
	pwm_reverse.ChangeDutyCycle(0)
	time.sleep(1)
	
except:
	KeyboardInterrupt("Test ended")
	
finally:
	pwm_forward.stop()
	pwm_reverse.stop()
	GPIO.cleanup()
