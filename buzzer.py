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
        self.pwm = GPIO.PWM(pin, 1000)
        self.pwm.start(0)
    
    def beep(self, frequency, duration=0.1):
        self.pwm.ChangeFrequency(frequency)
        self.pwm.ChangeDutyCycle(50)
        time.sleep(duration)
        self.pwm.ChangeDutyCycle(0)
    
    def connect_sound(self):
        self.beep(3500, 0.1)
        time.sleep(0.05)
        self.beep(4000, 0.1)
        time.sleep(0.05)
        self.beep(4500, 0.15)
    
    def disconnect_sound(self):
        self.beep(4500, 0.1)
        time.sleep(0.05)
        self.beep(4000, 0.1)
        time.sleep(0.05)
        self.beep(3500, 0.15)
    
    def drive_mode_sound(self):
        self.beep(4500, 0.08)
        time.sleep(0.08)
        self.beep(4500, 0.08)
    
    def hitch_mode_sound(self):
        self.beep(3500, 0.08)
        time.sleep(0.08)
        self.beep(3500, 0.08)
    
    def error_sound(self):
        for _ in range(3):
            self.beep(4000, 0.1)
            time.sleep(0.05)
    
    def cleanup(self):
        self.pwm.ChangeDutyCycle(0)
        self.pwm.stop()
