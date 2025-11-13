"""
motor driver class for BTS7960 motor controllers
controls one motor
"""
import RPi.GPIO as GPIO
import time

class MotorDriver:
    def __init__(self, rpwm_pin, lpwm_pin, name="Motor", acceleration=300):
        """
        initialize motor driver.
        
        Args:
            rpwm_pin: GPIO pin for forward control (RPWM on BTS7960)
            lpwm_pin: GPIO pin for reverse control (LPWM on BTS7960)
            name: Name for this motor (for debugging)
        """
        self.rpwm_pin = rpwm_pin
        self.lpwm_pin = lpwm_pin
        self.name = name
        
        self.acceleration = acceleration
        
        # speed tracking
        self.current_speed = 0
        self.target_speed = 0
        self.last_update_time = time.time()
        
        # setup GPIO pins
        GPIO.setup(rpwm_pin, GPIO.OUT)
        GPIO.setup(lpwm_pin, GPIO.OUT)
        
        # create PWM objects (1000 Hz frequency)
        self.pwm_forward = GPIO.PWM(rpwm_pin, 10000)
        self.pwm_reverse = GPIO.PWM(lpwm_pin, 10000)
        
        # start PWM at 0% duty cycle
        self.pwm_forward.start(0)
        self.pwm_reverse.start(0)
        
    def _set_speed_instant(self, speed):
        # clamp speed to valid range
        speed = max(-100, min(100, speed))
        
        if speed > 0:
            # forward
            self.pwm_reverse.ChangeDutyCycle(0)
            self.pwm_forward.ChangeDutyCycle(speed)
        elif speed < 0:
            # reverse
            self.pwm_forward.ChangeDutyCycle(0)
            self.pwm_reverse.ChangeDutyCycle(abs(speed))
        else:
            # stop
            self.pwm_forward.ChangeDutyCycle(0)
            self.pwm_reverse.ChangeDutyCycle(0)
            
    def update(self):
        if self.current_speed == self.target_speed:
            return
        
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now
        
        if dt <= 0:
            return
            
        max_change = self.acceleration * dt
        
        diff = self.target_speed - self.current_speed
        
        if abs(diff) <= max_change:
            self.current_speed = self.target_speed
        else:
            if diff > 0:
                self.current_speed += max_change
            else:
                self.current_speed -= max_change
            
        self._set_speed_instant(self.current_speed)
    
    def set_speed(self, speed):
        self.target_speed = max(-100, min(100, speed))
        
    def set_speed_instant(self, speed):
        speed = max(-100, min(100, speed))
        self.target_speed = speed
        self.current_speed = speed
        self._set_speed_instant(speed)
        
    def set_acceleration(self, acceleration):
        self.acceleration = max(1, acceleration)
        
    def stop(self):
        """stop the motor"""
        self.set_speed(0)
    
    def emergency_stop(self):
        """emergency stop - no ramping"""
        self.set_speed_instant(0)
    
    
    def cleanup(self):
        """clean up PWM and GPIO"""
        self.emergency_stop()
        self.pwm_forward.stop()
        self.pwm_reverse.stop()
            

