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
            r_en_pin: GPIO pin for right enable (R_EN on BTS7960) - optional
            l_en_pin: GPIO pin for left enable (L_EN on BTS7960) - optional
            name: Name for this motor (for debugging)
        """
        self.rpwm_pin = rpwm_pin
        self.lpwm_pin = lpwm_pin
        # self.r_en_pin = r_en_pin
        # self.l_en_pin = l_en_pin
        self.name = name
        
        # setup GPIO pins
        GPIO.setup(rpwm_pin, GPIO.OUT)
        GPIO.setup(lpwm_pin, GPIO.OUT)

        """
        if r_en_pin is not None:
            GPIO.setup(r_en_pin, GPIO.OUT)
            GPIO.output(r_en_pin, GPIO.HIGH)
        
        if l_en_pin is not None:
            GPIO.setup(l_en_pin, GPIO.OUT)
            GPIO.output(l_en_pin, GPIO.HIGH)
        """
        
        # create PWM objects (1000 Hz frequency)
        self.pwm_forward = GPIO.PWM(rpwm_pin, 10000)
        self.pwm_reverse = GPIO.PWM(lpwm_pin, 10000)
        
        # start PWM at 0% duty cycle
        self.pwm_forward.start(0)
        self.pwm_reverse.start(0)
    
    def set_speed(self, speed):
        """
        set motor speed
        
        Args:
            speed: -100 to 100
                   positive = forward
                   negative = reverse
                   0 = stop
        """
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
    
    def stop(self):
        """stop the motor"""
        self.set_speed(0)
    
    def cleanup(self):
        """clean up PWM and GPIO"""
        self.pwm_forward.stop()
        self.pwm_reverse.stop()

        """
        if self.r_en_pin is not None:
            GPIO.output(self.r_en_pin, GPIO.LOW)
        if self.l_en_pin is not None:
            GPIO.output(self.l_en_pin, GPIO.LOW)
        """
            

