# simple_led_test.py
# Minimal test - just drive LEDs with controller, no extra features

import RPi.GPIO as GPIO
import time
from motor_driver_led import MotorDriver  # LED version
from controller import BluetoothController
from differential_steering import DifferentialSteering

print("=" * 70)
print("SIMPLE LED + CONTROLLER TEST")
print("=" * 70)
print("\nWiring:")
print("  Front Left:  Red=GPIO3, Green=GPIO4")
print("  Front Right: Red=GPIO15, Green=GPIO18")
print("  Rear Left:   Red=GPIO9, Green=GPIO11")
print("  Rear Right:  Red=GPIO23, Green=GPIO24")
print()

GPIO.setmode(GPIO.BCM)

# Initialize LED "motors"
print("Setting up LED motors...")
motor_fl = MotorDriver(3, 4, "Front Left")
motor_fr = MotorDriver(15, 18, "Front Right")
motor_rl = MotorDriver(9, 11, "Rear Left")
motor_rr = MotorDriver(23, 24, "Rear Right")

# Initialize controller and steering
print("\nConnecting controller...")
controller = BluetoothController()
print("✅ Controller connected!")

steering = DifferentialSteering(pivot_y_limit=25)

print("\n" + "=" * 70)
print("READY! Move left joystick to control LEDs")
print("Press Ctrl+C to exit")
print("=" * 70)
print()

try:
    while True:
        # Read controller
        controller.read_events()
        forward, turn = controller.get_drive_values()
        
        # Calculate motor speeds
        left_speed, right_speed = steering.compute_motors(turn, forward)
        
        # Apply to LEDs
        motor_fl.set_speed(left_speed)
        motor_rl.set_speed(left_speed)
        motor_fr.set_speed(right_speed)
        motor_rr.set_speed(right_speed)
        
        # Show values
        print(f"Joy: X={turn:4d} Y={forward:4d} | "
              f"Left={left_speed:4.0f} Right={right_speed:4.0f}",
              end='\r')
        
        time.sleep(0.02)

except KeyboardInterrupt:
    print("\n\nStopping...")

finally:
    motor_fl.stop()
    motor_fr.stop()
    motor_rl.stop()
    motor_rr.stop()
    
    motor_fl.cleanup()
    motor_fr.cleanup()
    motor_rl.cleanup()
    motor_rr.cleanup()
    
    print("✅ Done")