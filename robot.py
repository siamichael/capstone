"""
robot control class
manages 4 individual motors and actuator, uses differential steering
"""
import RPi.GPIO as GPIO
from motor_driver import MotorDriver
from differential_steering import DifferentialSteering

class Robot:
    def __init__(self):
        """initialize the device"""
        GPIO.setmode(GPIO.BCM)
        
        # initialize motor drivers
        self.motor_front_left = MotorDriver(3, 4, "Front Left", 400)
        self.motor_front_right = MotorDriver(15, 18, "Front Right", 400)
        self.motor_rear_left = MotorDriver(9, 11, "Rear Left", 400)
        self.motor_rear_right = MotorDriver(23, 24, "Rear Right", 400)
        self.actuator = MotorDriver(19, 26, "Actuator", 400)
        
        # initialize differential steering algo
        self.steering = DifferentialSteering(pivot_y_limit=25)
        
        # speed limit (0-100)
        self.max_speed = 100
        
        # track actuator position (approximate)
        self.actuator_position = 0  # 0 = fully down, 100 = fully up
        self.actuator_limit = 18  # 18 inches of travel
    
    def update(self):
        self.motor_front_left.update()
        self.motor_front_right.update()
        self.motor_rear_left.update()
        self.motor_rear_right.update()
        self.actuator.update()
        
    def drive(self, x_input, y_input):
        """
        drive the robot using differential steering
        
        Args:
            x_input: Turn value (-100 to 100)
                    negative = turn left
                    positive = turn right
            y_input: Forward/backward value (-100 to 100)
                    negative = reverse
                    positive = forward
        """
        # speed limit
        y_input = y_input * self.max_speed / 100
        
        # compute motor speeds using differential steering algo
        left_speed, right_speed = self.steering.compute_motors(x_input, y_input)
        
        self.motor_front_left.set_speed(left_speed)
        self.motor_rear_left.set_speed(left_speed)
        self.motor_front_right.set_speed(right_speed)
        self.motor_rear_right.set_speed(right_speed)
    
    def set_max_speed(self, speed_percent):
        """
        set max speed limit
        
        Args:
            speed_percent: 0-100, percentage of full speed
        """
        self.max_speed = max(0, min(100, speed_percent))
        print(f"Max speed set to {self.max_speed}%")
    
    def set_drive_acceleration(self, acceleration):
        self.motor_front_left.set_acceleration(acceleration)
        self.motor_front_right.set_acceleration(acceleration)
        self.motor_rear_left.set_acceleration(acceleration)
        self.motor_rear_right.set_acceleration(acceleration)
    
    def set_actuator_acceleration(self, acceleration):
        self.actuator.set_acceleration(acceleration)
    
    def raise_tongue(self, speed=50):
        """
        raise the trailer tongue
        
        Args:
            speed: 0-100, speed of actuator
        """
        self.actuator.set_speed(-speed)
    
    def lower_tongue(self, speed=50):
        """
        lower the trailer tongue.
        
        Args:
            speed: 0-100, speed of actuator (positive, will be reversed internally)
        """
        self.actuator.set_speed(speed)
    
    def stop_actuator(self):
        self.actuator.stop()
    
    def stop_all(self):
        """emergency stop - stop all motors immediately"""
        self.motor_front_left.stop()
        self.motor_front_right.stop()
        self.motor_rear_left.stop()
        self.motor_rear_right.stop()
        self.actuator.stop()
    
    def cleanup(self):
        """clean up GPIO pins."""
        self.motor_front_left.cleanup()
        self.motor_front_right.cleanup()
        self.motor_rear_left.cleanup()
        self.motor_rear_right.cleanup()
        self.actuator.cleanup()
        GPIO.cleanup()
        print("GPIO cleanup complete")
