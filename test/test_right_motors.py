import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import RPi.GPIO as GPIO
from controller import BluetoothController
from motor_driver import MotorDriver
from differential_steering import DifferentialSteering

GPIO.setmode(GPIO.BCM)

motor_front_right = MotorDriver(15, 18, "Front Right")
motor_rear_right = MotorDriver(23, 24, "Rear Right")

steering = DifferentialSteering(pivot_y_limit=25)

print("Connecting to controller...")
try:
    controller = BluetoothController()
except Exception as e:
    print(f"ERROR: {e}")
    GPIO.cleanup()
    exit(1)

max_speed = 100
last_command_time = time.time()
command_timeout = 1.5

try:
    while True:
        if not controller.is_connected():
            print("\nController disconnected")
            break
        
        controller.read_events()
        
        forward, turn = controller.get_drive_values()
        
        if controller.received_events_this_frame or controller.has_input():
            last_command_time = time.time()
        
        if time.time() - last_command_time > command_timeout:
            motor_front_right.stop()
            motor_rear_right.stop()
        else:
            y_input = forward * max_speed / 100
            
            left_speed, right_speed = steering.compute_motors(turn, y_input)
            
            motor_front_right.set_speed(right_speed)
            motor_rear_right.set_speed(right_speed)
            
            print(f"Joystick: Y={forward:4d} X={turn:4d} → Right motor: {right_speed:4.0f}%", end='\r')
        
        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n\nTest stopped")

finally:
    motor_front_right.stop()
    motor_rear_right.stop()
    motor_front_right.cleanup()
    motor_rear_right.cleanup()
    GPIO.cleanup()
    print("\nCleanup complete")
