# motor_driver_led.py
# LED version of motor driver for testing
# Use this for LED test, then use real motor_driver.py for robot

import RPi.GPIO as GPIO

class MotorDriver:
    """
    LED motor driver for testing
    Simulates motor with 2 LEDs (forward and reverse)
    """
    
    def __init__(self, forward_pin, reverse_pin, name="Motor"):
        """
        Initialize LED motor driver
        
        Args:
            forward_pin: GPIO pin for forward LED (simulates R_PWM)
            reverse_pin: GPIO pin for reverse LED (simulates L_PWM)
            name: Motor name for debugging
        """
        self.forward_pin = forward_pin
        self.reverse_pin = reverse_pin
        self.name = name
        
        # Setup GPIO
        GPIO.setup(forward_pin, GPIO.OUT)
        GPIO.setup(reverse_pin, GPIO.OUT)
        
        # Setup PWM (1000 Hz)
        self.forward_pwm = GPIO.PWM(forward_pin, 1000)
        self.reverse_pwm = GPIO.PWM(reverse_pin, 1000)
        
        # Start at 0%
        self.forward_pwm.start(0)
        self.reverse_pwm.start(0)
        
        print(f"  ✅ {name}: Forward=GPIO{forward_pin}, Reverse=GPIO{reverse_pin}")
    
    def set_speed(self, speed):
        """
        Set motor speed (-100 to +100)
        Positive = forward (red LED)
        Negative = reverse (green LED)
        """
        speed = max(-100, min(100, speed))  # Clamp to -100 to 100
        
        if speed > 0:
            # Forward - red LED
            self.forward_pwm.ChangeDutyCycle(abs(speed))
            self.reverse_pwm.ChangeDutyCycle(0)
        elif speed < 0:
            # Reverse - green LED
            self.forward_pwm.ChangeDutyCycle(0)
            self.reverse_pwm.ChangeDutyCycle(abs(speed))
        else:
            # Stop - both off
            self.forward_pwm.ChangeDutyCycle(0)
            self.reverse_pwm.ChangeDutyCycle(0)
    
    def stop(self):
        """Stop motor (turn off LEDs)"""
        self.forward_pwm.ChangeDutyCycle(0)
        self.reverse_pwm.ChangeDutyCycle(0)
    
    def cleanup(self):
        """Clean up GPIO"""
        self.forward_pwm.stop()
        self.reverse_pwm.stop()
        GPIO.cleanup()


# For compatibility with your existing code
# This makes the LED version work exactly like the real version