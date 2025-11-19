"""
buzzer module for audio feedback
provides beeps for mode changes and connection status
"""
import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, pin=27):
        """
        initialize buzzer
        
        Args:
            pin: GPIO pin number for buzzer
        """
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 2000)
        self.pwm.start(0)
    
    def beep(self, duration=0.1):
        self.pwm.ChangeDutyCycle(50)
        time.sleep(duration)
        self.pwm.ChangeDutyCycle(0)
    
    def double_beep(self):
        self.beep(0.1)
        time.sleep(0.1)
        self.beep(0.1)
    
    def connect_sound(self):
        self.pwm.ChangeFrequency(1000)
        self.beep(0.15)
        time.sleep(0.05)
        self.pwm.ChangeFrequency(1500)
        self.beep(0.15)
        self.pwm.ChangeFrequency(2000)
    
    def disconnect_sound(self):
        self.pwm.ChangeFrequency(1500)
        self.beep(0.15)
        time.sleep(0.05)
        self.pwm.ChangeFrequency(1000)
        self.beep(0.15)
        self.pwm.ChangeFrequency(2000)
    
    def drive_mode_sound(self):
        self.pwm.ChangeFrequency(2500)
        self.double_beep()
        self.pwm.ChangeFrequency(2000)
    
    def hitch_mode_sound(self):
        self.pwm.ChangeFrequency(1500)
        self.double_beep()
        self.pwm.ChangeFrequency(2000)
    
    def cleanup(self):
        self.pwm.stop()