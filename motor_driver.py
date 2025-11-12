"""
motor driver class for BTS7960 motor controllers
controls one motor
"""
import RPi.GPIO as GPIO

class MotorDriver:
    def __init__(self, rpwm_pin, lpwm_pin, name="Motor"):
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
        self.ramp_time = 0.3
        self.current_speed = 0
        
        # setup GPIO pins
        GPIO.setup(rpwm_pin, GPIO.OUT)
        GPIO.setup(lpwm_pin, GPIO.OUT)
        
        # create PWM objects (1000 Hz frequency)
        self.pwm_forward = GPIO.PWM(rpwm_pin, 10000)
        self.pwm_reverse = GPIO.PWM(lpwm_pin, 10000)
        
        # start PWM at 0% duty cycle
        self.pwm_forward.start(0)
        self.pwm_reverse.start(0)
        
    def _ramp_speed(self, start_speed, end_speed):
        if self.ramp_time <= 0:
            self.set_speed_instant(end_speed)
            return
        
        steps = 20
        delay = self.ramp_time / steps
        
        for i in range(steps + 1):
            current = start_speed + (end_speed - start_speed) * (i / steps)
            self._set_speed_instant(current)
            time.sleep(delay)
            
    
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
    
    def set_speed(self, speed):
        self._ramp_speed(self.current_speed, speed)
        self.current_speed = speed
        
    def set_speed_instant(self, speed):
        self._set_speed_instant(self.current_speed, speed)
        self.current_speed = speed
        
    def stop(self):
        """stop the motor"""
        self.set_speed(0)
        
    def emergency_stop(self):
        """emergency stop - no ramping"""
        self.set_speed_instant(0)
    
    def cleanup(self):
        """clean up PWM and GPIO"""
        self.pwm_forward.stop()
        self.pwm_reverse.stop()
            

